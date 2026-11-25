from dataclasses import dataclass, field

from libs.dtos.entity import EntityToClientDTO
from libs.math import Position2, Vector2


@dataclass
class PlayerLoadDTO:
    """Data Transfer Object for player loading data."""
    race: str
    attributes: dict[str, list[int | float]]
    to_first_lvlup: int
    raising_xp: float
    xp_boost: float


@dataclass
class ClientPlayerDTO:
    """State of the local player sent from the server to the client."""
    name: str
    id: int
    position: Position2
    orientation: Vector2
    xp: "ProgressBar"
    lvl: int
    map_block: str
    body: list[EntityToClientDTO] = field(default_factory=list)
