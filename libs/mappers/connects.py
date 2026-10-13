from dataclasses import dataclass

from libs import Version
from libs.mappers import ClientPlayerMapper
from libs.dtos import (
    ConnectServerDTO, ConnectClientDTO,
    GameDataToServerDTO, GameDataToClientDTO,
)
from libs.mappers.entity import EntityToClientMapper
from libs.math import Position2, Vector2


@dataclass(frozen=True, slots=True)
class ConnectServerMapper:
    """Mapper for server connection data.

    This class provides static methods to convert between ConnectServerDTO
    and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: ConnectServerDTO) -> dict[str, str]:
        """Converts a ConnectServerDTO to a dictionary.

        Args:
            dto (ConnectServerDTO): The server connection data DTO.

        Returns:
            dict[str, str]: A dictionary representation of the server connection data.
        """
        return {
            "version": str(dto.version),
            "name": dto.name,
        }

    @staticmethod
    def dict_to_dto(data: dict) -> ConnectServerDTO:
        """Converts a dictionary to a ConnectServerDTO.

        Args:
            data (dict): The dictionary containing server connection data.

        Returns:
            ConnectServerDTO: The reconstructed ConnectServerDTO.
        """
        return ConnectServerDTO(
            name=data["name"],
            version=Version(data["version"]),
        )

@dataclass(frozen=True, slots=True)
class ConnectClientMapper:
    """Mapper for client connection data.

    This class provides static methods to convert between ConnectClientDTO
    and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: ConnectClientDTO) -> dict[str, str]:
        """Converts a ConnectClientDTO to a dictionary.

        Args:
            dto (ConnectClientDTO): The client connection data DTO.

        Returns:
            dict[str, str]: A dictionary representation of the client connection data.
        """
        return {
            "version": str(dto.version),
            "name": dto.name,
            "password": dto.password
        }

    @staticmethod
    def dict_to_dto(data: dict) -> ConnectClientDTO:
        """Converts a dictionary to a ConnectClientDTO.

        Args:
            data (dict): The dictionary containing client connection data.

        Returns:
            ConnectClientDTO: The reconstructed ConnectClientDTO.
        """
        return ConnectClientDTO(
            name=data["name"],
            version=Version(data["version"]),
            password=data["password"]
        )

@dataclass(frozen=True, slots=True)
class GameDataToServerMapper:
    """Mapper for game data sent to the server.

    This class provides static methods to convert between GameDataToServerDTO
    and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: GameDataToServerDTO) -> dict[str, str | float | int |  None]:
        """Converts a GameDataToServerDTO to a dictionary.

        Args:
            dto (GameDataToServerDTO): The game data DTO.

        Returns:
            dict[str, str]: A dictionary representation of the game data.
        """
        return {
            "move": str(dto.move),
            "speed": dto.speed,
            "target_position": str(dto.target_position),
            "action": dto.action
        }

    @staticmethod
    def dict_to_dto(data: dict[str, list[float | int] | float | int | str]) -> GameDataToServerDTO:
        """Converts a dictionary to a GameDataToServerDTO.

        Args:
            data (dict[str, list[float] | float | str]): The dictionary containing game data.

        Returns:
            GameDataToServerDTO: The reconstructed GameDataToServerDTO.
        """
        return GameDataToServerDTO(
            move=Vector2(data["move"]),
            speed=data["speed"],
            target_position=Position2(data["target_position"]),
            action=data["action"]
        )

@dataclass(frozen=True, slots=True)
class GameDataToClientMapper:
    """Mapper for game data sent to the client.

    This class provides static methods to convert between GameDataToClientDTO
    and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: GameDataToClientDTO) -> dict[str, str | list | dict]:
        """Converts a GameDataToClientDTO to a dictionary.

        Args:
            dto (GameDataToClientDTO): The game data DTO.

        Returns:
            dict[str, str]: A dictionary representation of the game data.
        """
        return {
            "map_block": dto.map_block,
            "entities": [EntityToClientMapper.dto_to_dict(g) for g in dto.entities],
            "player": ClientPlayerMapper.dto_to_dict(dto.player),
            "chunk_position": str(dto.chunk_position),
            "position": str(dto.position),
        }

    @staticmethod
    def dict_to_dto(data: dict) -> GameDataToClientDTO:
        """Converts a dictionary to a GameDataToClientDTO.

        Args:
            data (dict): The dictionary containing game data.

        Returns:
            GameDataToClientDTO: The reconstructed GameDataToClientDTO.
        """
        return GameDataToClientDTO(
            map_block=data["map_block"],
            entities=[EntityToClientMapper.dict_to_dto(g) for g in data["entities"]],
            player=ClientPlayerMapper.dict_to_dto(data["player"]),
            chunk_position=Position2(data["chunk_position"]),
            position=Position2(data["position"]),
        )
