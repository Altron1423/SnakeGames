from dataclasses import dataclass
from libs import Version
from .entity import EntityToClientDTO
from libs.dtos.player import ClientPlayerDTO
from libs.math import Position2, Vector2


@dataclass
class AddressConnectDTO:
    """Data Transfer Object for connection address information.

    Attributes:
        ip (str): IP address.
        port (int | None): Port number. Defaults to None.
        mac (str | None): MAC address. Defaults to None.
    """
    ip: str
    port: int | None = None
    mac: str | None = None


@dataclass
class ConnectServerDTO:
    """Data Transfer Object for server connection information.

    Attributes:
        version (Version): The version of the client.
        name (str): Name of the client.
        address (AddressConnectDTO | None): Connection address. Defaults to None.
    """
    version: Version
    name: str
    address: AddressConnectDTO | None = None


@dataclass
class ConnectClientDTO:
    """Data Transfer Object for client connection information.

    Attributes:
        version (Version): The version of the server.
        name (str): Name of the client.
        password (str): Connection password.
    """
    version: Version
    name: str
    password: str


@dataclass
class GameDataToServerDTO:
    """Data Transfer Object for game data sent from client to server.

    Attributes:
        move (Vector2): Movement vector.
        speed (float): Current speed.
        target_position (Position2): Target position.
        action (str | None): Current action being performed. Defaults to None.
    """
    move: Vector2
    speed: float
    target_position: Position2
    action: str | None = None


@dataclass
class GameDataToClientDTO:
    """Data Transfer Object for game data sent from server to client.

    Attributes:
        map_block (str): Description or identifier of the map block.
        entities (list[EntityToClientDTO]): List of entities in the vicinity.
        player (ClientPlayerDTO): Player-specific information.
        chunk_position (Position2): Position of the chunk.
        position (Position2): Position of the entity.
    """
    map_block: str
    entities: list[EntityToClientDTO]
    player: ClientPlayerDTO
    chunk_position: Position2
    position: Position2
