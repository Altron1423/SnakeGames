from dataclasses import dataclass, field
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
    """Состояние игрока, передаваемое от сервера клиенту."""
    name: str
    id: int
    position: Position2
    xp: "ProgressBar"
    lvl: int
    map_block: str
    body: list[Position2] = field(default_factory=list)
    direction: Vector2 = field(default_factory=lambda: Vector2(0, 1))
