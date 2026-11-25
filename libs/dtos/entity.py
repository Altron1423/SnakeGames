from __future__ import annotations

from dataclasses import dataclass

from libs.math import Position2, Vector2


@dataclass
class EntityToClientDTO:
    """Data for an entity sent to a client, including optional child segments."""

    name: str
    id: int
    position: Position2
    orientation: Vector2
    visual_action: str
    body: list[EntityToClientDTO] | None = None
