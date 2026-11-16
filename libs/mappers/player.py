from dataclasses import dataclass

from libs.dtos import PlayerLoadDTO, ClientPlayerDTO
from libs.math import Position2, Vector2


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
            "xp": str(dto.xp),
            "lvl": dto.lvl,
            "map_block": dto.map_block,
            "body": [str(segment) for segment in dto.body],
            "direction": str(dto.direction),
        }

    @staticmethod
    def dict_to_dto(data: dict) -> ClientPlayerDTO:
        from libs import ProgressBar

        body_data = data.get("body")
        body = (
            [Position2(segment) for segment in body_data]
            if body_data
            else [Position2(data["position"])]
        )
        direction_data = data.get("direction")

        return ClientPlayerDTO(
            name=data["name"],
            id=data["id"],
            position=Position2(data["position"]),
            xp=ProgressBar.init_from_str(data["xp"]),
            lvl=data["lvl"],
            map_block=data["map_block"],
            body=body,
            direction=(
                Vector2(direction_data)
                if direction_data
                else Vector2(0, 1)
            ),
        )
