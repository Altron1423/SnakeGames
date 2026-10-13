import pygame as pg


class Styler:
    """Manages colors and fonts for UI elements.

    Attributes:
        id (int): Unique identifier.
        stylers (list[Styler]): List of all styler instances.
        color (tuple): Primary color.
        color_select (tuple): Color when selected.
        color_clicked (tuple): Color when clicked.
        color_off (tuple): Color when off.
        font_color (tuple): Font color.
        font_name (str): Font name.
        font_size (int): Font size.
        font (pg.font.Font): Pygame font object.
    """
    id = 0
    stylers = []

    def __init__(self):
        """Initializes the Styler."""
        self._set_id()
        self.color = (255, 0, 0)
        self.color_select = (0, 255, 0)
        self.color_clicked = (0, 0, 255)
        self.color_off = (0, 0, 0)
        self.font_color = (255, 255, 255)

        self.font_name = 'Comic Sans MS'
        self.font_size = 30
        self.font = pg.font.SysFont(self.font_name, self.font_size)

    def set_color(self, param: int, color: tuple | None):
        """Sets one of the colors.

        Args:
            param (int): The color index (0: color, 1: color_select, 2: color_clicked, 3: color_off, 4: font_color).
            color (tuple | None): The color value.
        """
        if color is not None:
            if param == 0:
                self.color = color
            elif param == 1:
                self.color_select = color
            elif param == 2:
                self.color_clicked = color
            elif param == 3:
                self.color_off = color
            elif param == 4:
                self.font_color = color

    def set_font(self, name: str | None = None, size: int | None = None):
        """Sets the font name and/or size.

        Args:
            name (str | None): The font name.
            size (int | None): The font size.
        """
        if name is not None:
            self.font_name = name
        if size is not None:
            self.font_size = size
        if name is not None or size is not None:
            self.font = pg.font.SysFont(self.font_name, self.font_size)

    def text_render(self, text: str):
        """Renders text using the current font and color.

        Args:
            text (str): The text to render.

        Returns:
            pg.Surface | None: The rendered text surface, or None if text is empty.
        """
        if text:
            return self.font.render(text, True, self.font_color)
        return None

    def _set_id(self):
        """Assigns an ID and adds this instance to the stylers list."""
        self.id = Styler.id
        Styler.id += 1
        Styler.stylers.append(self)

    @classmethod
    def load_json(cls, data: dict) -> "Styler":
        """Loads a Styler from a dictionary.

        Args:
            data (dict): The data containing 'colors' (list) and 'font' (list).

        Example:
            {"colors": [None, None, None, None, None], "font": ['arial', 25]}

        Returns:
            Styler: The loaded Styler.
        """
        style = Styler()
        for i in range(5):
            style.set_color(i, data["colors"][i])
        style.set_font(*data['font'])
        return style

    @classmethod
    def get_styler(cls, id: int) -> "Styler":
        """Gets a styler by its ID.

        Args:
            id (int): The styler ID.

        Returns:
            Styler: The styler object.
        """
        return cls.stylers[id]
