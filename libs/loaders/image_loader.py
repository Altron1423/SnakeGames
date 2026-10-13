from pathlib import Path
import pygame as pg
import json

from libs.loaders.loader import Loader


class ImageLoader(Loader):
    """A loader class for images.

    This class is responsible for loading image files and managing them in memory.
    """
    elements: dict[str, tuple[pg.Surface | None, str]]

    def load(self, path: Path) -> None:
        """Loads images from a specified path.

        Args:
            path (Path): The path to the file containing image information.
        """
        with path.open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "image":
                json_data = json_data["images"]
                for name in json_data:
                    image = [None, json_data[name]]
                    self.add(image, name)

    def get(self, name: str) -> pg.Surface | None:
        """Retrieves an image by name.

        Args:
            name (str): The name of the image.

        Returns:
            pg.Surface | None: The image surface if loaded, otherwise None.
        """
        image = self.elements.get(name)
        if image is None:
            return None
        elif image[0] is None:
            image[0] = pg.image.load(Path.cwd().joinpath(image[1]))
        return image[0]


image_loader = ImageLoader()
