from libs.graphics.Bars import Bars
from libs.math import Size2, Position2, Recalc
from libs.window.Mouse import Mouse
from libs.graphics.TriggerGen import TriggerGen
from libs.graphics.interface_elements import Button, PngElement, TextElement
from libs.graphics.polygons import ManyPolygonizer
import pygame as pg


class ButtonManager:
    """Manages a collection of interactive UI elements on a surface.

    Attributes:
        _buttons (list[Button]): List of all buttons managed by this manager.
        polygonizer (ManyPolygonizer): Polygonizer used for collision detection.
        mouse (Mouse): Mouse object for handling mouse input.
        last_polygonizer (ManyPolygonizer | None): The last used polygonizer.
        triggers (dict[int, Button]): Not directly used in current implementation.
        address (str): The current address/layer for the buttons.
        surface (pg.Surface | None): The surface where buttons are drawn.
        surface_size (Size2): The size of the surface.
        active_button (int | None): The index of the currently hovered button.
        dynamic_position_X (Bars): A bar for horizontal movement control.
        dynamic_position_Y (Bars): A bar for vertical movement control.
    """

    _buttons: list[Button]
    polygonizer: ManyPolygonizer
    mouse: Mouse
    last_polygonizer: ManyPolygonizer | None
    triggers: dict[int, Button]
    address: str
    surface: pg.Surface | None
    surface_size: Size2
    active_button: int | None
    dynamic_position_X: Bars
    dynamic_position_Y: Bars

    def __init__(self, mouse: Mouse):
        """Initializes the ButtonManager.

        Args:
            mouse (Mouse): The mouse object to track input.
        """
        self._buttons = []
        self.polygonizer = ManyPolygonizer(Size2(100, 100))
        self.mouse = mouse
        self.last_polygonizer = None
        self.address = "main"
        self.surface = None
        self.active_button = None
        self.dynamic_position_X = Bars(0, 0, 0)
        self.dynamic_position_Y = Bars(0, 0, 0)

    def set_surface(self, surface: pg.Surface):
        """Sets the surface for buttons to be drawn on.

        Args:
            surface (pg.Surface): The target surface.
        """
        self.surface = surface
        self.surface_size = Size2(surface.get_size())
        for button in self._buttons:
            button.set_surface_size(self.surface_size)

    def set_address(self, new_address: str):
        """Sets the current address for the manager.

        Args:
            new_address (str): The new address.
        """
        self.address = new_address

    def set_polygonizer(self, polygonizer: ManyPolygonizer):
        """Sets the polygonizer used for collision detection.

        Args:
            polygonizer (ManyPolygonizer): The polygonizer to use.
        """
        self.last_polygonizer = polygonizer

    def set_move_limit_x(self, lim: float):
        """Sets the limit for the horizontal dynamic position bar.

        Args:
            lim (float): The new limit.
        """
        self.dynamic_position_X.setLimit(lim)

    def set_move_limit_y(self, lim: float):
        """Sets the limit for the vertical dynamic position bar.

        Args:
            lim (float): The new limit.
        """
        self.dynamic_position_Y.setLimit(lim)

    def add_button(self, text: str, position: Recalc, size: Recalc, triggers: TriggerGen | None) -> Button:
        """Adds a standard button to the manager.

        Args:
            text (str): The text displayed on the button.
            position (Recalc): The position of the button.
            size (Recalc): The size of the button.
            triggers (TriggerGen | None): The triggers for the button.

        Returns:
            Button: The created button.
        """
        button = self._create_button("button")
        button.set_text(text)
        button.set_button_position_size(position, size)
        self.set_triggers(button, triggers)
        return button

    def add_text(self, text: str, position: Recalc, size: Recalc) -> TextElement:
        """Adds a text element to the manager.

        Args:
            text (str): The text content.
            position (Recalc): The position.
            size (Recalc): The size.

        Returns:
            TextElement: The created text element.
        """
        button: Button | PngElement | TextElement = self._create_button("txt")
        button.set_text(text)
        button.set_button_position_size(position, size)
        # button.move_to(position[:2])
        # button.resize(position[2:])
        return button

    def add_png(self, position: Recalc, size: Recalc, png: pg.Surface) -> PngElement:
        """Adds a PNG image element to the manager.

        Args:
            position (Recalc): The position.
            size (Recalc): The size.
            png (pg.Surface): The image surface.

        Returns:
            PngElement: The created PNG element.
        """
        button = self._create_button()
        button.set_type("png")
        if len(position) == 1:
            position = [*position, *png.get_size()]
        button.set_button_position_size(position, size)
        button.set_png(png)
        return button

    def add_png_but(self, position: Recalc, size: Recalc, triggers: TriggerGen, png: pg.Surface):
        """Adds a button with a PNG background.

        Args:
            position (Recalc): The position.
            size (Recalc): The size.
            triggers (TriggerGen): The triggers for the button.
            png (pg.Surface): The image surface.
        """
        button = self._create_button("png_but")
        button.set_button_position_size(position, size)
        button.set_png(png)
        self.set_triggers(button, triggers)

        return button

    def add_mower(self, position: Recalc, size: Recalc, moveX: Bars | None = None, moveY: Bars | None = None):
        """Adds a 'mower' button for continuous movement.

        Args:
            position (Recalc): The position.
            size (Recalc): The size.
            moveX (Bars | None): The horizontal control bar.
            moveY (Bars | None): The vertical control bar.
        """
        button = self._create_button()
        button.set_type("mower")
        button.set_button_position_size(position, size)
        trigers = TriggerGen()

        if moveX is not None:
            mvX = moveX
            trigers.MWD(lambda x: moveX.add(-0.05 * moveX.getFull()[1]))
            trigers.MWU(lambda x: moveX.add(0.05 * moveX.getFull()[1]))
        else:
            mvX = None

        if moveY is not None:
            mvY = moveY
            trigers.MWD(lambda x: moveY.add(-0.05 * moveY.getFull()[1]))
            trigers.MWU(lambda x: moveY.add(0.05 * moveY.getFull()[1]))
        else:
            mvY = None

        button.set_triggers(trigers)
        button.set_mover(mvX, mvY)

    def key_interact(self, key: int, is_down: bool):
        """Handles key press and release events.

        Args:
            key (int): The pygame key constant.
            is_down (bool): True if key is pressed, False if released.
        """
        for i_button in self._buttons:
            called = i_button.triggers[(key, is_down)]
            if called is not None:
                called(i_button)

    def set_triggers(self, button: Button, triggers: TriggerGen):
        """Assigns triggers to a button.

        Args:
            button (Button): The button to assign triggers to.
            triggers (TriggerGen): The triggers object.
        """
        button.set_triggers(triggers)

    def get_button(self, index: int | None) -> Button | None:
        """Gets a button by its index.

        Args:
            index (int | None): The index of the button.

        Returns:
            Button | None: The button at the given index, or None.
        """
        if index is not None:
            return self._buttons[index]
        return None

    def cleen_buttons(self):
        """Clears all buttons from the manager."""
        self._buttons = []

    def select(self, event: pg.event.Event):
        """Handles mouse click events.

        Args:
            event (pg.event.Event): The mouse event.
        """
        but = event.button
        up = event.type == pg.MOUSEBUTTONDOWN
        button: Button = self.get_button(self.active_button)
        if button is not None:
            button.select((but, up))

    def draw(self):
        """Draws all managed buttons on the surface."""
        if self.surface is not None:
            mouse_pos = self.mouse.get_position(self.address)
            if mouse_pos in self.surface_size:
                pass
            else:
                mouse_pos = Position2(-1000, 1000)
            self.active_button = self._testing_activ(mouse_pos)
            self.mouse.add_button(self.get_button(self.active_button))
            for i, butt in enumerate(self._buttons):
                butt.draw(self.surface, self.active_button == i)

    def _testing_activ(self, mouse_pos: Position2) -> int | None:
        """Helper to find the button currently under the mouse.

        Args:
            mouse_pos (Position2): The current mouse position.

        Returns:
            int | None: The index of the hovered button, or None.
        """
        last = None
        for i, butt in enumerate(self._buttons):
            if butt.test_active(mouse_pos):
                last = i
        return last

    def _create_button(self, type_button="button") -> Button:
        """Factory method to create buttons.

        Args:
            type_button (str): The type of button to create.

        Returns:
            Button | PngElement: The newly created button element.

        Raises:
            ValueError: If the type_button is not recognized.
        """
        if type_button == "button":
            button = Button(self, len(self._buttons))
        elif type_button == "mower":
            button = Button(self, len(self._buttons))
        elif type_button == "png":
            button = PngElement(self, len(self._buttons))
        elif type_button == "txt":
            button = TextElement(self, len(self._buttons))
        elif type_button == "png_but":
            button = PngElement(self, len(self._buttons))
        else:
            raise ValueError(f"Unknown button type: {type_button}")

        self._buttons.append(button)

        if self.last_polygonizer is not None:
            button.set_polygonizer(self.last_polygonizer)
        else:
            button.set_polygonizer(self.polygonizer)

        if self.surface is not None:
            button.set_surface_size(self.surface_size)

        return button
