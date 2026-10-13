import pygame as pg

from libs.Loger import loger
from libs.graphics.styler import Styler

from libs.math import Recalc, Size2, Position2, Vector2


class Resizer:
    """A class to manage resizing of positions and sizes.

    Attributes:
        position (Position2): The current position.
        size (Size2): The current size.
        recalc_position (Recalc | None): The recalculation rule for position.
        recalc_size (Recalc | None): The recalculation rule for size.
        surface_size (Size2 | None): The size of the surface.
    """
    position: Position2
    size: Size2
    recalc_position: Recalc | None
    recalc_size: Recalc | None
    surface_size: Size2 | None

    def __init__(self, recalc_position: Recalc, recalc_size: Recalc):
        """Initializes the Resizer.

        Args:
            recalc_position (Recalc): The rule for position recalculation.
            recalc_size (Recalc): The rule for size recalculation.
        """
        self.surface_size = None
        self.set_recalc_position(recalc_position)
        self.set_recalc_size(recalc_size)

    def _recalculation_positions(self):
        """Recalculates the position based on the surface size."""
        if self.surface_size is not None:
            self.position = self.recalc_position.value(self.surface_size)

    def _recalculation_size(self):
        """Recalculates the size based on the surface size."""
        if self.surface_size is not None:
            self.size = self.recalc_size.value(self.surface_size)

    def set_surface_size(self, surface_size: Size2):
        """Sets the surface size and triggers recalculation.

        Args:
            surface_size (Size2): The new surface size.
        """
        self.surface_size = surface_size
        self._recalculation_size()
        self._recalculation_positions()

    def set_recalc_position(self, recalc_position: Recalc | None):
        """Sets the rule for position recalculation.

        Args:
            recalc_position (Recalc | None): The new rule for position.

        Raises:
            TypeError: If recalc_position is not Recalc and not None.
        """
        if isinstance(recalc_position, Recalc):
            self.recalc_position = recalc_position
            self._recalculation_positions()
        elif recalc_position is None:
            pass
        else:
            raise TypeError(f"{recalc_position} not {Recalc._type_}")

    def set_recalc_size(self, recalc_size: Recalc | None):
        """Sets the rule for size recalculation.

        Args:
            recalc_size (Recalc | None): The new rule for size.

        Raises:
            TypeError: If recalc_size is not Recalc and not None.
        """
        if isinstance(recalc_size, Recalc):
            self.recalc_size = recalc_size
            self._recalculation_positions()
        elif recalc_size is None:
            pass
        else:
            raise TypeError(f"{recalc_size} not {Recalc._type_}")

    def move_to(self, position: Position2):
        """Moves the position to a new position using a recalculation rule.

        Args:
            position (Position2): The new target position.
        """
        self.recalc_position = Recalc(Vector2(), position)

    def move_on(self, d_position: Position2):
        """Moves the position relative to current position.

        Args:
            d_position (Position2): The relative movement.
        """
        self.recalc_position += d_position

    def resize(self, new_size: Recalc):
        """Sets a new size rule.

        Args:
            new_size (Recalc): The new size rule.
        """
        self.recalc_size = new_size


class Polygon(Resizer):
    """A geometric polygon used for UI elements.

    Attributes:
        id (int): Unique identifier.
        type (int | None): Type of polygon (1: rect, 2: text, 3: png).
        _png (pg.Surface | None): The PNG image.
        _pngTr (pg.Surface | None): The PNG image with transparency?
        _pngRect (pg.Rect | None): The rect of the PNG.
        _text (str | None): The text content.
        option_surfaces (pg.Surface | None): A surface for rendering options.
        border (bool): Whether to draw a border.
    """
    id = 0
    type: int | None = None
    _png: pg.Surface | None = None
    _pngTr: pg.Surface | None = None
    _pngRect: pg.Rect | None = None
    _text: str | None = None
    option_surfaces: pg.Surface | None = None
    border: bool = False

    def __init__(self, position: Recalc, size: Recalc):
        """Initializes a Polygon.

        Args:
            position (Recalc): Position rule.
            size (Recalc): Size rule.
        """
        super().__init__(position, size)
        self.styler = Styler()
        self._set_id()
        self.type = None
        self._png = None
        self._pngTr = None
        self._pngRect = None
        self._text = None
        self.option_surfaces = None
        self.border = False

    def draw(self, surface: pg.Surface, status):
        """Draws the polygon on the surface.

        Args:
            surface (pg.Surface): The target surface.
            status (Any): The current status (color/effect).
        """
        option_rect = (*self.position.tuple, *self.size.tuple)
        if self.type is None:
            pass
        elif self.type == 1:
            color = self._get_color(status)
            if len(color) == 3:
                pg.draw.rect(surface, color, option_rect, self.border)
            else:
                sr = pg.Surface(self.size.tuple)
                sr.fill(color[:3])
                sr.set_alpha(color[3])
                surface.blit(sr, self.position.tuple)
        elif self.type == 2:
            if self._text is not None:
                surface.blit(self.option_surfaces, option_rect)

        elif self.type == 3:
            if self._png is not None:
                surface.blit(self._pngTr, option_rect)


    def set_style(self, style):
        self.styler = style
        self.option_surfaces = self.styler.text_render(self._text)

    def set_text(self, text:str):
        self._text = text
        # self.option_surfaces = self.styler.text_render(self.text)
        self.blit_text()

    def set_png(self, png):
        self._png = png
        self._resize_png()


    def resize(self, new_size):
        super().resize(new_size)
        self._resize_png()
        self.blit_text()

    def set_recalc_size(self, recalc: Recalc):
        super().set_recalc_size(recalc)
        self._resize_png()
        self.blit_text()

    def set_surface_size(self, surface_size):
        super().set_surface_size(surface_size)
        self._resize_png()
        self.blit_text()


    def __copy__(self):
        dp = DoterPolygon(self)
        return dp

    def _get_color(self, status):
        color = (3, 9, 200)
        match status:
            case 1:
                color = self.styler.color_off
            case 2:
                color = self.styler.color_clicked
            case 3:
                color = self.styler.color_select
            case 4:
                color = self.styler.color

        return color

    def _resize_png(self):
        if self._png is not None:
            # loger.log(self._png)
            self._pngTr = pg.transform.scale(self._png, self.size.tuple)
            self._pngRect = self._png.get_rect(topleft=(0,0))
        else:
            self._pngTr = None
            self._pngRect = None

    def _set_id(self):
        if not isinstance(self, DoterPolygon):
            self.id = Polygon.id
            Polygon.id += 1

    def blit_text(self):
        if self.surface_size is None:
            return
        surface = pg.Surface(self.surface_size.tuple, pg.SRCALPHA, 32)
        if self._text is not None:
            words = [word.split(' ') for word in self._text.splitlines()]
            space = self.styler.font.size(' ')[0]
            max_width, max_height = self.surface_size.x - 10, self.surface_size.z - 10
            x = y = 0
            word_width = word_height = 0
            for line in words:
                for word in line:
                    if word != "":
                        word_surface = self.styler.text_render(word)
                        word_width, word_height = word_surface.get_size()
                        if x + word_width >= max_width:
                            x = 0
                            y += word_height
                        surface.blit(word_surface, (x, y))
                        x += word_width + space
                    else:
                        x += space
                x = 0
                y += word_height
        self.option_surfaces = surface


    @classmethod
    def rect(cls, recalc_position:Recalc=None, recalc_size:Recalc=None):
        if recalc_position is None:
            recalc_position = Recalc()
        if recalc_size is None:
            recalc_size = Recalc()
        polygon = cls(recalc_position, recalc_size)
        polygon.type = 1
        return polygon

    @classmethod
    def text(cls, text, recalc_position:Recalc=None, recalc_size:Recalc=None):
        if recalc_position is None:
            recalc_position = Recalc()
        if recalc_size is None:
            recalc_size = Recalc()
        polygon = cls(recalc_position, recalc_size)
        polygon.type = 2
        polygon.set_text(text)
        return polygon

    @classmethod
    def png(cls, png, recalc_position:Recalc=None, recalc_size:Recalc=None):
        if recalc_position is None:
            recalc_position = Recalc()
        if recalc_size is None:
            recalc_size = Recalc()
        polygon = cls(recalc_position, recalc_size)
        polygon.type = 3
        polygon.set_png(png)
        return polygon

    @classmethod
    def load_json(cls, data:dict) -> "Polygon":
        """
        {"type": 1, "position": [0,0], "size": [0,0], "percent_position": [None,None], "percent_size": [None,None], "styleID": 0, "border": None, "text": None, "png": None}

        :param data: 
        :return: 
        """
        if data["type"] == 1:
            polygon = Polygon.rect()
        elif data["type"] == 2:
            polygon = Polygon.text(data.get("text"))
        elif data["type"] == 3:
            from libs.loaders.image_loader import image_loader
            image = image_loader.get(data["pngName"])
            loger.log(image)
            polygon = Polygon.png(image)
        else:
            loger.log(f"ERROR TYPE {data['type']=}")
            raise

        if data.get("position") is not None:
            polygon.set_recalc_position(Recalc.load_from_str(data["position"]))
        if data.get("size") is not None:
            polygon.set_recalc_size(Recalc.load_from_str(data["size"]))

        if data.get("styleID") is not None:
            polygon.set_style(Styler.get(data["styleID"]))
        elif data.get("styleName") is not None:
            from libs.loaders.styler_loader import styler_loader
            polygon.set_style(styler_loader.get(data["styleName"]))
        if data.get("border") is not None:
           polygon.border = data["border"]

        return polygon


class DoterPolygon(Polygon):
    def __init__(self, main_polygon: Polygon):
        self.main_polygon = main_polygon
        super().__init__(main_polygon.recalc_position, main_polygon.recalc_size)
        self.id = main_polygon.id
        self.percent_position = None
        self.percent_size = None
        self.surface_size = None
        self.styler = None
        self.type = None
        self.border = None
        self.percent_use = None

    def __getattribute__(self, item):
        att = object.__getattribute__(self, item)
        if att is None:
            att = getattr(self.main_polygon, item)
        return att


class ManyPolygonizer(Resizer):
    """A collection of polygons.

    Attributes:
        polygons (list[Polygon]): List of polygons.
        surface (pg.Surface): The aggregated surface.
        status (Any): Current status for rendering.
        last_status (Any): The last status used.
        main_png (Polygon | None): The main PNG polygon.
        main_text (Polygon | None): The main text polygon.
    """
    def __init__(self, size: Size2):
        """Initializes a ManyPolygonizer.

        Args:
            size (Size2): The size of the aggregated surface.
        """
        super().__init__(Recalc(), Recalc(Vector2(1,1)))
        self.polygons: list[Polygon] = []
        self.surface = pg.Surface(size.tuple)
        self.status = None
        self.last_status = None
        self.main_png = None
        self.main_text = None

    def _redraw(self):
        """Redraws the aggregated surface."""
        self.surface = pg.Surface(self.size.tuple, pg.SRCALPHA, 32)
        for polygon in self.polygons:
            polygon.draw(self.surface, self.status)

    def reset_status(self, status: Any):
        """Resets the status.

        Args:
            status (Any): The new status.
        """
        self.status = status

    def set_surface_size(self, surface_size: Size2):
        """Sets the surface size and resizes all polygons.

        Args:
            surface_size (Size2): The new surface size.
        """
        super().set_surface_size(surface_size)
        for polygon in self.polygons:
            polygon.set_surface_size(surface_size)
        self._redraw()

    def add_polygon(self, polygon: Polygon):
        """Adds a polygon to the collection.

        Args:
            polygon (Polygon): The polygon to add.
        """
        self.polygons.append(polygon)
        polygon.set_surface_size(self.size)
        if polygon.type == 2:
            if self.main_text is None:
                self.main_text = polygon.id
        elif polygon.type == 3:
            if self.main_png is None:
                self.main_png = polygon.id

    def get_surf(self) -> pg.Surface:
        """Gets the aggregated surface, redrawing if status changed.

        Returns:
            pg.Surface: The aggregated surface.
        """
        if self.status != self.last_status:
            self.last_status = self.status
            self._redraw()
        return self.surface

    def get_polygon(self, id: int) -> Polygon | None:
        """Gets a polygon by its ID.

        Args:
            id (int): The polygon ID.

        Returns:
            Polygon | None: The polygon if found, else None.
        """
        for polygon in self.polygons:
            if polygon.id == id:
                return polygon
        return None

    def __iadd__(self, other: ManyPolygonizer):
        """Merges another ManyPolygonizer into this one.

        Args:
            other (ManyPolygonizer): The other polygonizer.
        """
        self.polygons += other.polygons

    def __copy__(self) -> "DoterPolygons":
        """Creates a copy using DoterPolygons.

        Returns:
            DoterPolygons: A copy.
        """
        return DoterPolygons(self)

    @classmethod
    def load_json(cls, data: dict) -> "ManyPolygonizer":
        """Loads a ManyPolygonizer from a dictionary.
        Example:
            {"polygons": [], "size": [25, 25]}

        Args:
            data (dict): The data containing size and polygons.

        Returns:
            ManyPolygonizer: The loaded polygonizer.
        """
        many_polygon = cls(Size2())
        many_polygon.set_surface_size(Size2(data["size"]))
        for i in data["polygons"]:
            polygon = Polygon.load_json(i)
            many_polygon.add_polygon(polygon)
        return many_polygon


class DoterPolygons(ManyPolygonizer):
    """A proxy for ManyPolygonizer to allow easy access to main_polygonizer attributes.

    Attributes:
        main_polygonizer (ManyPolygonizer): The original polygonizer.
    """
    def __init__(self, main_polygonizer: ManyPolygonizer):
        """Initializes the DoterPolygons proxy.

        Args:
            main_polygonizer (ManyPolygonizer): The original polygonizer.
        """
        self.main_polygonizer = main_polygonizer
        super().__init__(Size2(10, 10))
        self.polygons = []
        for polygon in self.main_polygonizer.polygons:
            pl = polygon.__copy__()
            self.polygons.append(pl)

        self.surface = None
        self.status = None
        self.last_status = None

    def __getattribute__(self, item):
        att = object.__getattribute__(self, item)
        if att is None:
            att = getattr(self.main_polygonizer, item)
        return att
