from libs.graphics.styler import Styler
from pathlib import Path
import json

from libs.loaders.loader import Loader

if __name__ == '__main__':
    import pygame as pg
    pg.init()

class StylerLoader(Loader):
    """A loader class for stylers.

    This class is responsible for loading styler data from files.
    """
    elements: dict[str, Styler]

    def load(self, path: Path) -> None:
        """Loads stylers from a specified path.

        Args:
            path (Path): The path to the file containing styler data.
        """
        with path.open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "styler":
                json_data = json_data["styles"]
                for name in json_data:
                    style = Styler.load_json(json_data[name])
                    self.add(style, name)

    def get(self, name: str) -> Styler | None:
        """Retrieves a loaded styler by name.

        Args:
            name (str): The name of the styler.

        Returns:
            Styler | None: The styler object if found, otherwise None.
        """
        return super().get(name)


styler_loader = StylerLoader()

if __name__ == "__main__":
    path = Path(r"C:\Users\Altron\PycharmProjects\MMO_project\src\data\configs\styles_config.json")
    styler_loader.load(path)
