import pygame as pg
from libs.math import Position2

class Mouse:
    """Manages mouse interaction and position tracking across multiple screens.

    Attributes:
        mouse (pg.mouse): The Pygame mouse module.
        absolute (Position2): The absolute mouse position on the screen.
        position_on_screen (Position2): The mouse position relative to the main screen.
        shift_main_screen (Position2): The shift applied to the mouse position for the main screen.
        scale (int): The scaling factor for the mouse position.
        address_data (dict[str, Screen]): A mapping of screen names to their Screen data.
        buttons (list): A list of active buttons.
    """


    mouse: pg.mouse
    absolute: Position2
    position_on_screen: Position2
    shift_main_screen: Position2
    scale: int
    address_data: dict[str, Screen]
    buttons: list

    def __init__(self):
        """Initializes the Mouse instance with default values.
        """
        self.mouse = pg.mouse
        self.absolute = Position2(-1, -1)
        self.position_on_screen = Position2(-1, -1)
        self.shift_main_screen = Position2(0, 0)
        self.scale = 1
        self.address_data = {}
        self.buttons = []

    def set_absolute(self, position: Position2):
        """Sets the absolute mouse position and updates the on-screen position.

        Args:
            position (Position2): The new absolute mouse position.
        """
        self.absolute = position
        self.position_on_screen = (self.absolute - self.shift_main_screen) // self.scale

    def update_screen_data(self, shift_position: Position2, scale: int = None, address: str = "main"):
        """Updates the scaling and shift parameters for a specific screen address.

        Args:
            shift_position (Position2): The shift to apply to the screen.
            scale (int, optional): The new scale factor. Defaults to None.
            address (str): The name of the screen address. Defaults to "main".
        """
        if address == "main":
            if scale is not None:
                self.scale = scale
            self.shift_main_screen = shift_position
        elif address in self.address_data.keys():
            self.address_data[address].move(shift_position)
            self.address_data[address].rescale(scale)

    def update(self):
        """Updates the mouse position based on current mouse state.
        """
        if self.mouse.get_focused():
            self.set_absolute(self.__get_mouse_position__())
        else:
            self.set_absolute(Position2(-1, -1))

    def get_position(self, address_screen: str = "main"):
        """Gets the mouse position for a specific screen address.

        Args:
            address_screen (str): The screen address to get the position for. Defaults to "main".

        Returns:
            Position2: The mouse position for the given address.
        """
        if address_screen == "main":
            position = self.position_on_screen
        elif address_screen in self.address_data.keys():
            scale = self.address_data[address_screen].scale
            shift = self.address_data[address_screen].shift
            position = (self.position_on_screen - shift) // scale
        else:
            position = Position2(-1, -1)

        return position

    def add_address(self, address, data):
        """Adds a new screen address with the provided parameters.

        Args:
            address (str): The name of the new address.
            data (dict): Parameters to initialize the Screen object.
        """
        screen = self.Screen()
        screen.set_parameters(**data)
        self.address_data[address] = screen

    def add_button(self, button):
        """Adds a button to the list of active buttons.

        Args:
            button: The button to add.
        """
        if button is not None:
            self.buttons.append(button)

    def interactive(self, event):
        """Processes interaction events like mouse button presses.

        Args:
            event (pygame.event.Event): The event to process.
        """
        if event.type == 1025:  # MOUSEBUTTONDOWN
            self.select(event.button)
        elif event.type == 1026:  # MOUSEBUTTONUP
            self.unselect(event.button)
            self.un_hold()

    def select(self, button):
        """Selects a button.

        Args:
            button: The button to select.
        """
        ...

    def unselect(self, button):
        """Unselects a button.

        Args:
            button: The button to unselect.
        """
        ...

    def un_hold(self):
        """Resets all held buttons and clears the buttons list.
        """
        for button in self.buttons:
            button.un_hold()
        self.buttons = []

    def __get_mouse_position__(self):
        """Gets the current mouse position from pygame.

        Returns:
            Position2: The current mouse position.
        """
        return Position2(*self.mouse.get_pos())

    class Screen:
        """Represents the mouse state for a specific screen.

        Attributes:
            shift (Position2): The shift applied to the screen.
            scale (int): The scale factor for the screen.
            scaling (bool): Whether the screen is currently scaling.
        """
        shift: Position2
        scale: int
        scaling: bool

        def __init__(self):
            """Initializes the Screen instance with default values.
            """
            self.shift = Position2(0, 0)
            self.scale = 1
            self.scaling = False

        def set_parameters(self, shift: Position2 = None, scale: int = None, scaling: bool = None):
            """Sets the parameters for the screen.

            Args:
                shift (Position2, optional): The shift to set. Defaults to None.
                scale (int, optional): The scale to set. Defaults to None.
                scaling (bool, optional): The scaling state to set. Defaults to None.
            """
            if shift is not None:
                self.shift = shift
            if scale is not None:
                self.scale = scale
            if scaling is not None:
                self.scaling = scaling

        def rescale(self, scale: int):
            """Rescales the screen.

            Args:
                scale (int): The new scale factor.
            """
            self.scale = scale

        def move(self, position: Position2):
            """Moves the screen's shift position.

            Args:
                position (Position2): The new shift position.
            """
            self.shift = position
