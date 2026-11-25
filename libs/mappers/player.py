from dataclasses import dataclass

from libs.dtos import PlayerLoadDTO, ClientPlayerDTO
from libs.math import Position2, Vector2
from .entity import EntityToClientMapper


@dataclass(frozen=True, slots=True)
class PlayerLoadMapper:
    """Mapper for player load data."""

    @staticmethod
    def dto_to_dict(dto: PlayerLoadDTO) -> dict[str, str | dict | int | float]:
        return {
            "race": dto.race,
            "attributes": dto.attributes,
            "to_first_lvlup": dto.to_first_lvlup,
            "raising_xp": dto.raising_xp,
            "xp_boost": dto.xp_boost,
        }

    @staticmethod
    def dict_to_dto(data: dict) -> PlayerLoadDTO:
        return PlayerLoadDTO(
            race=data["race"],
            attributes=data["attributes"],
            to_first_lvlup=data["to_first_lvlup"],
            raising_xp=data["raising_xp"],
            xp_boost=data["xp_boost"],
        )


@dataclass(frozen=True, slots=True)
class ClientPlayerMapper:
    """Mapper for player state transferred from the server to a client."""

    @staticmethod
    def dto_to_dict(dto: ClientPlayerDTO) -> dict:
        return {
            "name": dto.name,
            "id": dto.id,
            "position": str(dto.position),
            "orientation": str(dto.orientation),
            "xp": str(dto.xp),
            "lvl": dto.lvl,
            "map_block": dto.map_block,
            "body": [
                EntityToClientMapper.dto_to_dict(segment)
                for segment in dto.body
            ],
        }

    @staticmethod
    def dict_to_dto(data: dict) -> ClientPlayerDTO:
        from libs import ProgressBar

        body = [
            EntityToClientMapper.dict_to_dto(segment)
            for segment in data.get("body", [])
        ]

        return ClientPlayerDTO(
            name=data["name"],
            id=data["id"],
            position=Position2(data["position"]),
            orientation=Vector2(data["orientation"]),
            xp=ProgressBar.init_from_str(data["xp"]),
            lvl=data["lvl"],
            map_block=data["map_block"],
            body=body,
        )
