import json
from pathlib import Path
import pygame as pg

from . import Loader
from .image_loader import image_loader
from ..mappers import TileMapMapper

def f(value: int, name: str) -> str | None:
    """Returns the name if value is 1, otherwise None.

    Args:
        value (int): The value to check.
        name (str): The name to return.

    Returns:
        str | None: The name if value is 1, otherwise None.
    """
    if value == 1:
        return name
    else:
        return None

T = tuple[str, str]
T2 = tuple[T, T]


class TileMapLoader(Loader):
    """A loader class for tile maps.

    This class is responsible for loading tile map data from files and
    creating tile surfaces.
    """
    elements: dict[T2, pg.Surface]

    def load(self, path: Path) -> None:
        """Loads a tile map from a specified path.

        Args:
            path (Path): The path to the file containing tile map data.
        """
        with path.open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "tile_map":
                data = TileMapMapper.dict_to_dto(json_data["data"])
                size = data.size
                image = image_loader.get(data.texture)
                for tile in data.tiles:
                    tile_r = (
                        (f(tile[0][0], data.name), f(tile[0][1], data.name)),
                        (f(tile[1][0], data.name), f(tile[1][1], data.name))
                    )
                    pos = data.tiles[tile]
                    surf = pg.Surface(data.size.tuple, pg.SRCALPHA)
                    surf.blit(
                        image,
                        (
                            -size.x * pos.x,
                            -size.z * pos.z
                        )
                    )
                    self.add(surf, tile_r)

    def add(self, surf: pg.Surface, tile_r: T2) -> None:
        """Adds a tile surface to the elements dictionary.

        Args:
            surf (pg.Surface): The surface to add.
            tile_r (T2): The tile identifier.
        """
        self.elements[tile_r] = surf

    def get(self, name: T2) -> pg.Surface | None:
        """Retrieves a loaded tile surface by its identifier.

        Args:
            name (T2): The tile identifier.

        Returns:
            pg.Surface | None: The tile surface if found, otherwise None.
        """
        element = self.elements.get(name)
        return element


tile_map_loader = TileMapLoader()
