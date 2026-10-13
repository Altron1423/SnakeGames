from dataclasses import dataclass

from ..math import Size2, Position2
from libs.dtos import (
    TileMapDTO
)


@dataclass(frozen=True, slots=True)
class TileMapMapper:
    """Mapper for tile map data.

    This class provides static methods to convert between TileMapDTO
    and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: TileMapDTO) -> dict[str, str | list]:
        """Converts a TileMapDTO to a dictionary.

        Args:
            dto (TileMapDTO): The tile map data DTO.

        Returns:
            dict[str, str]: A dictionary representation of the tile map data.
        """
        return {
            "name": dto.name,
            "texture": dto.texture,
            "size": str(dto.size),
            "tiles": []
        }

    @staticmethod
    def dict_to_dto(data: dict) -> TileMapDTO:
        """Converts a dictionary to a TileMapDTO.

        Args:
            data (dict): The dictionary containing tile map data.

        Returns:
            TileMapDTO: The reconstructed TileMapDTO.
        """
        tiles = {}
        for i in data["tiles"]:
            i2 = tuple(tuple(map(int, g.split(","))) for g in i.split("/"))
            tiles[i2] = Position2(data["tiles"][i])
        return TileMapDTO(
            name=data["name"],
            texture=data["texture"],
            size=Size2(data["size"]),
            tiles=tiles
        )
