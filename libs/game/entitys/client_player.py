from libs import GameDataToServerDTO, map_block_loader
from libs.dtos.player import ClientPlayerDTO
from libs.math import Vector2
from .client_enemy import ClientEnemy
from .player import Player


class ClientPlayer(Player):
    """Client-side player state and input handling."""

    entity_type: str = "ClientPlayer"
    body: list[ClientEnemy]

    def __init__(self, player_name: str):
        super().__init__()
        self.body = []
        self.raw_orientation = Vector2(0, 0)
        self.player_name = player_name
        self.last_direction_view = "down"

    def preferential_orientation(self) -> str:
        return f"{self.type_action}_{self.direction_view}"

    def get_data_from_server(self, dto: ClientPlayerDTO):
        self.name = dto.name
        self.id = dto.id
        self.position = dto.position
        self.orientation = dto.orientation
        self.xp = dto.xp
        self.lvl = dto.lvl
        self.map_block = map_block_loader.get(dto.map_block)
        self.body = ClientEnemy.update_segments(self.body, dto.body)

    def data_to_server(self) -> GameDataToServerDTO:
        return GameDataToServerDTO(
            game_tick=0,
            move=Vector2(self.orientation.x, self.orientation.z),
            action=None,
        )

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
