from dataclasses import dataclass

from libs.dtos import EntityToClientDTO
from libs.math import Position2, Vector2


@dataclass(frozen=True, slots=True)
class EntityToClientMapper:
    """Mapper for entity data sent to the client.

    This class provides static methods to convert between EntityToClientDTO
    and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: EntityToClientDTO) -> dict[str, str | int]:
        """Converts an EntityToClientDTO to a dictionary.

        Args:
            dto (EntityToClientDTO): The entity to client data DTO.

        Returns:
            dict[str, str]: A dictionary representation of the entity data.
        """
        return {
            "name": dto.name,
            "id": dto.id,
            "position": str(dto.position),
            "orientation": str(dto.orientation),
            "visual_action": dto.visual_action
        }

    @staticmethod
    def dict_to_dto(data: dict) -> EntityToClientDTO:
        """Converts a dictionary to an EntityToClientDTO.

        Args:
            data (dict): The dictionary containing entity data.

        Returns:
            EntityToClientDTO: The reconstructed EntityToClientDTO.
        """
        from libs import ProgressBar
        return EntityToClientDTO(
            name=data["name"],
            id=data["id"],
            position=Position2(data["position"]),
            orientation=Vector2(data["orientation"]),
            visual_action=data["visual_action"]
        )

