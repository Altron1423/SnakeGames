from __future__ import annotations

from libs import EntityToClientDTO, entity_animator_loader
from libs.math import Position2, Vector2
from .enemy import Enemy
from ...animator_controller import EntityAnimator


class ClientEnemy(Enemy):
    """Client-side entity with its own animator and optional child segments."""

    entity_type: str = "ClientEnemy"
    map_block_name: str
    target_position: Position2
    scaled_collision: Vector2
    last_direction_view: str
    animator: EntityAnimator | None
    body: list[ClientEnemy]

    def __init__(self, player_name: str):
        super().__init__()
        self.player_name = player_name
        self.animator = entity_animator_loader.get_new("player_animator")
        self.last_direction_view = "down"
        self.scaled_collision = self.collision * 1
        self.body = []

    @staticmethod
    def update_segments(
        current_segments: list[ClientEnemy],
        segment_data: list[EntityToClientDTO] | None,
    ) -> list[ClientEnemy]:
        """Updates existing client segment entities and creates only new ones."""
        existing_segments = {
            segment.id: segment for segment in current_segments
        }
        updated_segments = []

        for data in segment_data or []:
            segment = existing_segments.get(data.id)
            if segment is None:
                segment = ClientEnemy(str(data.id))
            segment.update_from_server(data)
            updated_segments.append(segment)

        return updated_segments

    def update_from_server(self, data: EntityToClientDTO):
        """Updates this entity and recursively synchronizes its body segments."""
        self.id = data.id
        self.name = data.name
        self.position = data.position
        self.health = getattr(data, "health", None)
        self.orientation = data.orientation
        self.body = self.update_segments(self.body, data.body)

        if self.animator is not None:
            self.animator.set_type(self.preferential_orientation)

    def set_scale(self, scale: float):
        if self.animator is not None:
            self.animator.set_scale(scale)
        self.scaled_collision = self.collision * scale

    @property
    def preferential_orientation(self) -> str:
        return f"{self.type_action}_{self.direction_view}"

    @property
    def direction_view(self) -> str:
        if self.orientation.x > 0:
            self.last_direction_view = "right"
        elif self.orientation.x < 0:
            self.last_direction_view = "left"
        elif self.orientation.z > 0:
            self.last_direction_view = "down"
        elif self.orientation.z < 0:
            self.last_direction_view = "up"
        return self.last_direction_view

    @property
    def type_action(self) -> str:
        if self.orientation.x != 0 or self.orientation.z != 0:
            if self.speed_control > 1:
                return "run"
            return "walk"
        return "idle"
