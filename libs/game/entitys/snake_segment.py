from libs.math import Position2, Vector2
from .entity import Entity


class SnakeSegment(Entity):
    """A single body segment that follows the player head."""

    entity_type: str = "SnakeSegment"

    def __init__(
        self,
        position: Position2 | None = None,
        orientation: Vector2 | None = None,
    ):
        super().__init__()
        self.free_moving = False
        self.speed = 0

        if position is not None:
            self.position = position.copy()
        if orientation is not None:
            self.orientation = orientation.copy()

    def __copy__(self) -> "SnakeSegment":
        """Creates an independent copy of this segment."""
        segment: SnakeSegment = super().__copy__()
        segment.position = self.position.copy()
        segment.orientation = self.orientation.copy()
        segment.map_block = self.map_block
        segment.free_moving = self.free_moving
        segment.speed = self.speed
        return segment
