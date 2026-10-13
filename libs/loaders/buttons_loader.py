from pathlib import Path
# from src import log
import json

from src import ButtonManager


class ButtonManagerLoader:
    """A loader class for buttons.

    This class is responsible for managing and loading buttons.
    """
    def __init__(self):
        self.buttons = {}

    def add_menu(self, menu, name):
        """Adds a menu to the buttons dictionary.

        Args:
            menu: The menu to add.
            name (str): The name associated with the menu.
        """
        self.buttons[name] = menu

    def load_images(self, path):
        """Loads images from a specified path.

        Args:
            path (Path): The path to the file containing image information.
        """
        with Path(path).open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "interface_elements":
                json_data = json_data["windows"]
                button_manager = ButtonManager(None)

                # for name in json_data:
                #     menu = [None, json_data[name]]
                #     self.add_menu(menu, name)
