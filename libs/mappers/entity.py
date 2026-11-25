from dataclasses import dataclass

from libs.dtos import EntityToClientDTO
from libs.math import Position2, Vector2


@dataclass(frozen=True, slots=True)
class EntityToClientMapper:
    """Mapper for entity data sent to the client."""

    @staticmethod
    def dto_to_dict(dto: EntityToClientDTO) -> dict:
        return {
            "name": dto.name,
            "id": dto.id,
            "position": str(dto.position),
            "orientation": str(dto.orientation),
            "visual_action": dto.visual_action,
            "body": (
                [EntityToClientMapper.dto_to_dict(segment) for segment in dto.body]
                if dto.body is not None
                else None
            ),
        }

    @staticmethod
    def dict_to_dto(data: dict) -> EntityToClientDTO:
        body_data = data.get("body")
        return EntityToClientDTO(
            name=data["name"],
            id=data["id"],
            position=Position2(data["position"]),
            orientation=Vector2(data["orientation"]),
            visual_action=data["visual_action"],
            body=(
                [EntityToClientMapper.dict_to_dto(segment) for segment in body_data]
                if body_data is not None
                else None
            ),
        )
