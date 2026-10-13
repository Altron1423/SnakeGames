from dataclasses import dataclass

from ..math import Size2, Position2

T = tuple[int, int]


@dataclass
class TileMapDTO:
    """Data Transfer Object for tile map data.

    Attributes:
        name (str): Name of the tile map.
        texture (str): Texture identifier.
        size (Size2): Size of the tile map.
        tiles (dict[tuple[T, T], Position2]): Dictionary mapping tile coordinates to position.
    """
    name: str
    texture: str
    size: Size2
    tiles: dict[
        tuple[T, T],
        Position2
    ]
