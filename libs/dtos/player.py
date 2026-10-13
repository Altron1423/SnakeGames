from dataclasses import dataclass
from libs.math import Position2, Vector2


@dataclass
class PlayerLoadDTO:
    """Data Transfer Object for player loading data.

    Attributes:
        race (str): Race of the player.
        attributes (dict[str, list[int | float]]): Attributes and their values.
        to_first_lvlup (int): Experience needed for the first level up.
        raising_xp (float): Rate of experience gain.
        xp_boost (float): Experience boost multiplier.
    """
    race: str
    attributes: dict[str, list[int | float]]
    to_first_lvlup: int
    raising_xp: float
    xp_boost: float


@dataclass
class ClientPlayerDTO:
    """Data Transfer Object for client-side player information.

    Attributes:
        name (str): Name of the player.
        id (int): Unique identifier of the player.
        attributes (dict[str, list[int | float]] | None): Player attributes.
        position (Position2): Current position of the player.
        health ("ProgressBar"): Health status.
        mana ("ProgressBar"): Mana status.
        xp ("ProgressBar"): Experience status.
        lvl (int): Player level.
        inventory (str): Inventory identifier.
        map_block (str): Map block identifier.
    """
    name: str
    id: int
    attributes: dict[str, list[int | float]] | None
    position: Position2
    health: "ProgressBar"
    mana: "ProgressBar"
    xp: "ProgressBar"
    lvl: int
    inventory: str
    map_block: str
