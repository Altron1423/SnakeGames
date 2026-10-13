import time
import pygame as pg

from libs.graphics.TriggerGen import TriggerGen
from libs.graphics.polygons import Resizer, ManyPolygonizer, Polygon, Recalc
from libs.graphics.Bars import Bars
from libs.math import Position2, Size2


if __name__ == "__main__":
    pg.init()


class Button(Resizer):
    """A specialized UI element that can be interacted with (clicked, hovered, held).

    Attributes:
        manager (ButtonManager): The manager that owns this button.
        id (int): Unique identifier for the button.
        polygons (ManyPolygonizer): Contains the geometric shapes of the button.
        type (str | None): The type of button (e.g., 'button', 'png', 'txt', 'mower').
        triggers (TriggerGen | None): The triggers containing event callbacks.
        text_polygon (Polygon | None): The polygon representing the button's text.
        png_polygon (Polygon | None): The polygon representing the button's image.
        visible (bool | None): Visibility state of the button.
        on (bool): Whether the button is enabled and can be interacted with.
        hold (bool): Whether the button is currently being held down.
        holding (bool): Internal state for the holding action.
        active (bool): Whether the button is currently hovered/active.
        active_time (float | None): Timestamp when the button became active.
        active_delta (float): Duration for the active state.
        description (str): Description of the button's purpose.
        parameters (dict): Additional parameters for the button.
        mvX (Bars | None): Horizontal control bar.
        mvY (Bars | None): Vertical control bar.
        mouse_position_on_button (list[int] | None): Localized mouse position.
    """
    manager: "ButtonManager"
    id: int
    polygons = ManyPolygonizer

    type: str | None
    triggers: TriggerGen | None

    text_polygon: Polygon | None
    png_polygon: Polygon | None

    visible: bool = None
    on: bool
    hold: bool
    holding: bool
    active: bool
    active_time: float | None
    active_delta: float
    description: str
    parameters: dict
    mvX: Bars | None
    mvY: Bars | None
    mouse_position_on_button: list[int] | None

    def __init__(self, manager, button_id):
        """Initializes a Button.

        Args:
            manager (ButtonManager): The manager this button belongs to.
            button_id (int): The unique ID for the button.
        """
        self.polygons = ManyPolygonizer(Size2())
        super().__init__(Recalc.default_very_faraway(), Recalc.default())

        self.manager = manager
        self.id = button_id

        self.function_active = None

        # self.type = "button"
        self.triggers = None
        self.png_polygon = None

        # self.visible = False
        self.on = True
        self.hold = False
        self.holding = False
        self.active = False
        self.active_time = False
        self.active_delta = 0.1
        self.description = ""
        self.parameters = {}

        self.mvX = self.mvY = None

    def get_parameters(self, name):
        """Gets a parameter by name.

        Args:
            name (str): The parameter name.

        Returns:
            Any: The parameter value.
        """
        return self.parameters.get(name)

    def set_parameters(self, name, parameters):
        """Sets a parameter by name.

        Args:
            name (str): The parameter name.
            parameters (Any): The parameter value.
        """
        self.parameters[name] = parameters

    def set_triggers(self, triggers):
        """Sets the triggers for the button.

        Args:
            triggers (TriggerGen): The triggers to assign.
        """
        self.triggers = triggers
        self.function_active = self._active_rect

    def set_holding(self, holding):
        """Sets the holding state.

        Args:
            holding (bool): The holding state.
        """
        self.holding = holding

    def set_work(self, work):
        """Sets whether the button is enabled.

        Args:
            work (bool): The work state.
        """
        self.on = work

    def set_visible(self, visible):
        """Sets the visibility of the button.

        Args:
            visible (bool): The visibility state.
        """
        self.visible = visible

    def set_polygonizer(self, polygonizer):
        """Sets the polygonizer for the button.

        Args:
            polygonizer (ManyPolygonizer): The polygonizer to use.
        """
        self.polygons = polygonizer.__copy__()
        if self.polygons.main_text is not None:
            self.text_polygon = self.polygons.get_polygon(self.polygons.main_text)
        if self.polygons.main_png is not None:
            self.png_polygon = self.polygons.get_polygon(self.polygons.main_png)

    def set_text(self, text: str):
        """Sets the text on the button.

        Args:
            text (str): The text to display.
        """
        if type(text) == str:
            self.text_polygon.set_text(text)
        self.polygons._redraw()

    def set_mover(self, mvX: None | Bars, mvY: None | Bars):
        """Sets the movement bars for the button.

        Args:
            mvX (Bars | None): The horizontal movement bar.
            mvY (Bars | None): The vertical movement bar.
        """
        self.mvX = mvX
        self.mvY = mvY

    def set_dynamic_position(self):
        """Placeholder for setting dynamic position."""
        ...

    def resize(self, size):
        """Resizes the button.

        Args:
            size (Size2): The new size.
        """
        super().resize(size)
        self.polygons.set_surface_size(size)

    def set_surface_size(self, surface_size):
        """Sets the surface size for the button.

        Args:
            surface_size (Size2): The new surface size.
        """
        super().set_surface_size(surface_size)
        self.polygons.set_surface_size(self.size)

    def set_button_position_size(self, position: Recalc, size: Recalc):
        """Sets both the position and size of the button.

        Args:
            position (Recalc): The position.
            size (Recalc): The size.
        """
        self.set_recalc_position(position)
        self.set_recalc_size(size)

    def _active_rect(self, mouse_position: Position2):
        """Checks if the mouse is within the button's bounds.

        Args:
            mouse_position (Position2): The mouse position.

        Returns:
            bool: True if the mouse is inside the button's area.
        """
        return mouse_position in self.size

    def test_active(self, mouse_position: Position2) -> bool:
        """Tests if the button should be considered active.

        Args:
            mouse_position (Position2): The current mouse position.

        Returns:
            bool: True if the button is active.
        """
        active = False
        mouse_position_on_button = mouse_position - self.position
        if self.on:
            if self.function_active is not None:
                active = self.function_active(mouse_position_on_button)
                if active:
                    self.mouse_position_on_button = mouse_position_on_button

            # if self.form == "rect":
            #     active = (
            #             0 <= mouse_position_on_button[0] <= self.size[0] and
            #             0 <= mouse_position_on_button[1] <= self.size[1]
            #     )
            # elif self.form == "circle":
            #     center_coordinate = [
            #         mouse_position_on_button[0] + self.size[0] // 2,
            #         mouse_position_on_button[1] + self.size[1] // 2
            #     ]
            #     active = center_coordinate[0] ** 2 + center_coordinate[1] ** 2 <= (self.size[0] // 2) ** 2

            if active and self.hold:
                self.active = True
                self.active_time = time.time() + self.active_delta

        return active

    def select(self, trigger: tuple[str, bool] | tuple[int, bool]):
        """Handles a button click/trigger event.

        Args:
            trigger (tuple): The trigger event (e.g., (key, is_down)).
        """
        if trigger[1] != self.hold:
            if self.triggers is not None:
                function = self.triggers[trigger]
                if function is not None:
                    function(self)
        self.hold = trigger[1]

    def un_hold(self):
        """Resets the hold state. (Placeholder)"""
        # function = self.triggers[('hold', False)]
        # if function is not None:
        #     function(self)
        self.hold = False

    def add_polygons(self, polygons):
        """Adds polygons to the button.

        Args:
            polygons (ManyPolygonizer): The polygons to add.
        """
        self.polygons += polygons

    def draw(self, surface: pg.Surface, activ: bool):
        """Draws the button on the surface.

        Args:
            surface (pg.Surface): The surface to draw on.
            activ (bool): Whether the button is currently being activated.
        """
        pg.draw.rect(surface, (0, 255, 0), (*self.position.tuple, *self.size.tuple))
        if self.visible:
            if not self.on:
                status = 1
            elif self.active:
                status = 2
                if self.active_time <= time.time():
                    self.active = False
            elif activ:
                status = 3
            else:
                status = 4

            self.polygons.reset_status(status)
            self.polygons._redraw()
            surface.blit(self.polygons.get_surf(), self.position.tuple)
        elif self.visible is None:
            if self.recalc_position is not None or self.recalc_size is not None:
                self.visible = True

        if self.on:
            if self.holding and self.hold and self.active:
                function = self.triggers[('hold', True)]
                if function is not None:
                    function(self)
