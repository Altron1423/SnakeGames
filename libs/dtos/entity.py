from dataclasses import dataclass

from libs.math import Position2, Vector2


@dataclass
class EntityToClientDTO:
    """Data Transfer Object for entity information sent to the client.

    The optional body and direction fields are populated for other players,
    allowing multiplayer clients to render their complete snakes.
    """
    name: str
    id: int
    position: Position2
    orientation: Vector2
    visual_action: str
    body: list[Position2] | None = None
