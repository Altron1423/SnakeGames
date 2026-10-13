from dataclasses import dataclass

from libs.dtos import (
    PlayerLoadDTO, ClientPlayerDTO
)
from libs.math import Position2


@dataclass(frozen=True, slots=True)
class PlayerLoadMapper:
    """Mapper for player load data.

    This class provides static methods to convert between PlayerLoadDTO
    and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: PlayerLoadDTO) -> dict[str, str | dict | int | float]:
        """Converts a PlayerLoadDTO to a dictionary.

        Args:
            dto (PlayerLoadDTO): The player load data DTO.

        Returns:
            dict[str, str | dict | int | float]: A dictionary representation of the player load data.
        """
        return {
            "race": dto.race,
            "attributes": dto.attributes,
            "to_first_lvlup": dto.to_first_lvlup,
            "raising_xp": dto.raising_xp,
            "xp_boost": dto.xp_boost,
        }

    @staticmethod
    def dict_to_dto(data: dict) -> PlayerLoadDTO:
        """Converts a dictionary to a PlayerLoadDTO.

        Args:
            data (dict): The dictionary containing player load data.

        Returns:
            PlayerLoadDTO: The reconstructed PlayerLoadDTO.
        """
        return PlayerLoadDTO(
            race=data["race"],
            attributes=data["attributes"],
            to_first_lvlup=data["to_first_lvlup"],
            raising_xp=data["raising_xp"],
            xp_boost=data["xp_boost"],
        )


@dataclass(frozen=True, slots=True)
class ClientPlayerMapper:
    """Mapper for client player data.

    This class provides static methods to convert between ClientPlayerDTO
    and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: ClientPlayerDTO) -> dict[str, str | int | dict]:
        """Converts a ClientPlayerDTO to a dictionary.

        Args:
            dto (ClientPlayerDTO): The client player data DTO.

        Returns:
            dict[str, str | int | dict]: A dictionary representation of the client player data.
        """
        return {
            "name": dto.name,
            "id": dto.id,
            "attributes": dto.attributes,
            "position": str(dto.position),
            "health": str(dto.health),
            "mana": str(dto.mana),
            "xp": str(dto.xp),
            "lvl": dto.lvl,
            "inventory": str(dto.inventory),
            "map_block": dto.map_block
        }

    @staticmethod
    def dict_to_dto(data: dict) -> ClientPlayerDTO:
        """Converts a dictionary to a ClientPlayerDTO.

        Args:
            data (dict): The dictionary containing client player data.

        Returns:
            ClientPlayerDTO: The reconstructed ClientPlayerDTO.
        """
        from libs import ProgressBar
        return ClientPlayerDTO(
            name=data["name"],
            id=data["id"],
            attributes=data["attributes"],
            position=Position2(data["position"]),
            health=ProgressBar.init_from_str(data["health"]),
            mana=ProgressBar.init_from_str(data["mana"]),
            xp=ProgressBar.init_from_str(data["xp"]),
            lvl=data["lvl"],
            inventory=data["inventory"],
            map_block=data["map_block"],
        )
