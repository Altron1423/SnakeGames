import json
from pathlib import Path
from libs import loger
from libs.graphics import ManyPolygonizer

from libs.loaders.loader import Loader

if __name__ == '__main__':
    import pygame as pg
    pg.init()

class ManyPolygonizerLoader(Loader):
    """A loader class for many polygonizers.

    This class is responsible for loading many polygonizer data from files.
    """
    elements: dict[str, ManyPolygonizer]

    def load(self, path: Path) -> None:
        """Loads many polygonizers from a specified path.

        Args:
            path (Path): The path to the file containing many polygonizers data.
        """
        with path.open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "ManyPolygonizer":
                json_data = json_data["many_polygonizers"]
                for name in json_data:
                    many_polygon = ManyPolygonizer.load_json(json_data[name])
                    self.add(many_polygon, name)
            else:
                loger.log(f"Uncorrected Type {json_data['type']}. Need type: \"ManyPolygonizer\"")

    def get(self, name: str) -> ManyPolygonizer | None:
        """Retrieves a many polygonizer by name.

        Args:
            name (str): The name of the many polygonizer.

        Returns:
            ManyPolygonizer | None: The many polygonizer object if found, otherwise None.
        """
        return super().get(name)


many_polygonizer_loader = ManyPolygonizerLoader()
if __name__ == "__main__":
    path = Path(r"C:\Users\Altron\PycharmProjects\MMO_project\src\data\configs\many_polygon_config.json")
    many_polygonizer_loader.load(path)
