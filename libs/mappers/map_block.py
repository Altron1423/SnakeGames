from dataclasses import dataclass

from libs import MapBlockSaveDTO, MapBlock, MapBlockConfigDTO
from libs.math import Position2


@dataclass(frozen=True, slots=True)
class MapBlockSaveMapper:
    """Mapper for map block saving data.

    This class provides static methods to convert between MapBlockSaveDTO,
    MapBlock objects, and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: MapBlockSaveDTO) -> dict:
        """Converts a MapBlockSaveDTO to a dictionary.

        Args:
            dto (MapBlockSaveDTO): The map block save data DTO.

        Returns:
            dict: A dictionary representation of the map block save data.
        """
        return {
            "full_name": dto.full_name,
            "name": dto.name,
            "id": dto.id,
            "position": dto.position,
            "chunks": dto.chunks
        }

    @staticmethod
    def dict_to_dto(data: dict) -> MapBlockSaveDTO:
        """Converts a dictionary to a MapBlockSaveDTO.

        Args:
            data (dict): The dictionary containing map block save data.

        Returns:
            MapBlockSaveDTO: The reconstructed MapBlockSaveDTO.
        """
        return MapBlockSaveDTO(
            full_name=data["full_name"],
            name=data["name"],
            id=data["id"],
            position=data["position"],
            chunks=data["chunks"]
        )

    @staticmethod
    def block_to_dto(map_block: MapBlock) -> MapBlockSaveDTO:
        """Converts a MapBlock object to a MapBlockSaveDTO.

        Args:
            map_block (MapBlock): The map block object.

        Returns:
            MapBlockSaveDTO: The reconstructed MapBlockSaveDTO.
        """
        return MapBlockSaveDTO(
            full_name=str(map_block),
            name=map_block.name,
            id=map_block.id,
            position=str(map_block.position),
            chunks=[
                [
                    str(chunk) if chunk else None
                    for chunk in line
                ]
                for line in map_block.form
            ]
        )

    @staticmethod
    def update_from_dto(block: MapBlock, dto: MapBlockSaveDTO):
        """Updates a MapBlock object from a MapBlockSaveDTO.

        Args:
            block (MapBlock): The map block object to update.
            dto (MapBlockSaveDTO): The map block save data DTO.
        """
        block.full_name = dto.full_name
        block.name = dto.name
        block.id = dto.id
        block.position = Position2(dto.position)

@dataclass(frozen=True, slots=True)
class MapBlockConfigMapper:

    @staticmethod
    def dict_to_dto(data: dict) -> MapBlockConfigDTO:
        return MapBlockConfigDTO(
            name=data["name"],
            size=data["size"],
            form=data["form"],
        )
