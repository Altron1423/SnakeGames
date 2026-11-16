from libs.math import Position2, Vector2
from ... import EntityToClientDTO, entity_animator_loader
from .enemy import Enemy
from ...animator_controller import EntityAnimator


class ClientEnemy(Enemy):
    """Client-side representation of another entity or player."""

    entity_type: str = "ClientEnemy"
    map_block_name: str
    target_position: Position2
    scaled_collision: Vector2
    last_direction_view: str
    animator: EntityAnimator

    def __init__(self, player_name: str):
        super().__init__()
        self.player_name = player_name
        self.animator = entity_animator_loader.get_new("player_animator")
        self.last_direction_view = "down"
        self.scaled_collision = self.collision * 1
        self.body: list[Position2] = []
        self.direction = Vector2(0, 1)

    def update_from_server(self, data: EntityToClientDTO):
        """Updates the entity, including a remote player's snake body."""
        self.position = data.position
        self.health = getattr(data, "health", None)
        self.orientation = data.orientation
        self.body = (
            [
                Position2(segment.x, segment.z)
                for segment in data.body
            ]
            if data.body is not None
            else []
        )
        self.direction = (
            Vector2(data.direction.x, data.direction.z)
            if data.direction is not None
            else Vector2(data.orientation.x, data.orientation.z)
        )
        if self.animator is not None:
            self.animator.set_type(self.preferential_orientation)

    def set_scale(self, scale: float):
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
