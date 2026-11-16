from libs import PLATE_SIZE, EntityToClientDTO
from libs.dtos import (
    ClientPlayerDTO,
    GameDataToServerDTO,
    GameDataToClientDTO,
    PlayerLoadDTO,
)
from libs.math import Position2, Vector2
from .entity import Entity


class Player(Entity):
    """Серверная модель игрока-змеи."""

    entity_type: str = "Player"
    free_moving: bool = False

    INITIAL_LENGTH = 3

    def __init__(self):
        super().__init__()
        self.speed = PLATE_SIZE

        # Координаты хранятся от головы к хвосту.
        self.direction = Vector2(0, 1)
        self.next_direction = Vector2(0, 1)
        self.body: list[Position2] = []
        self.last_game_tick = 0

    def set_default(self, name: str, spawn_position: Position2):
        """Задаёт имя, начальную позицию и формирует тело змеи."""
        self.name = name
        self.position = Position2(spawn_position.x, spawn_position.z)

        self.direction = Vector2(0, 1)
        self.next_direction = Vector2(0, 1)
        self.orientation = Vector2(self.direction.x, self.direction.z)

        self.body = [
            Position2(
                self.position.x - self.direction.x * self.speed * index,
                self.position.z - self.direction.z * self.speed * index,
            )
            for index in range(self.INITIAL_LENGTH)
        ]

    def set_changes_from_client(self, dto: GameDataToServerDTO):
        """Принимает только четыре направления движения по клеткам."""
        if dto.action != "select":
            return

        requested = dto.move
        is_cardinal = (
            (requested.x in (-1, 1) and requested.z == 0)
            or (requested.z in (-1, 1) and requested.x == 0)
        )
        if not is_cardinal:
            return

        requested = Vector2(int(requested.x), int(requested.z))

        # Разворот на 180 градусов запрещён.
        if requested == self.direction * -1:
            return

        self.next_direction = requested

    def update(self, game_tick: int):
        """Двигает голову и сдвигает за ней остальные сегменты один раз за тик."""
        if self.last_game_tick == game_tick:
            return

        self.last_game_tick = game_tick
        self.direction = Vector2(self.next_direction.x, self.next_direction.z)
        self.orientation = Vector2(self.direction.x, self.direction.z)

        next_position = self.position + self.direction * self.speed

        # Хвост освобождает клетку на этом шаге, поэтому входить в неё можно.
        if next_position in self.body[:-1]:
            return

        move_result, collected_fruit = self.__move_plate__()
        if move_result < 0:
            return

        self.body.insert(
            0,
            Position2(self.position.x, self.position.z)
        )

        if move_result == 1 and collected_fruit is not None:
            self.add_xp(collected_fruit.scored)

            # Убираем собранный фрукт с клетки, чтобы его нельзя было собрать повторно.
            _, fruit_plate, _ = self.__get_info_positon__(self.position)
            if collected_fruit in fruit_plate.entities:
                fruit_plate.entities.remove(collected_fruit)
        else:
            self.body.pop()

    def get_data_for_client(self, game_tick) -> GameDataToClientDTO:
        """Подготавливает состояние игрока и тела змеи для клиента."""
        return GameDataToClientDTO(
            game_tick=game_tick,
            map_block="",
            entities=self.map_block.get_entity_dto(),
            player=self.__player_data__,
            chunk_position=Position2(0, 0),
            position=self.position,
        )

    def get_light_data(self) -> EntityToClientDTO:
        """Передаёт тело змеи другим игрокам в многопользовательской игре."""
        return EntityToClientDTO(
            name=self.name,
            id=self.id,
            position=self.position,
            orientation=self.orientation,
            visual_action="walk",
            body=[
                Position2(segment.x, segment.z)
                for segment in self.body
            ],
            direction=Vector2(self.direction.x, self.direction.z),
        )

    def disconnect(self):
        """Removes the player from the current map block."""
        self.map_block.players_in_game.remove(self)

    def connect(self):
        """Adds the player to the current map block."""
        self.map_block.players_in_game.append(self)

    def get_near_entity(self, max_range: int) -> dict[str, int]:
        """Retrieves nearby entities within a certain range."""
        return self.map_block.get_near_entity(self.name, max_range)

    @classmethod
    def load_from_config(cls, dto: PlayerLoadDTO) -> "Player":
        """Loads the player's existing progression settings."""
        return super().load_from_config(dto)

    @property
    def __player_data__(self) -> ClientPlayerDTO:
        """Prepares player data for client-side representation."""
        return ClientPlayerDTO(
            name=self.name,
            id=self.id,
            position=Position2(self.position.x, self.position.z),
            xp=self.xp,
            lvl=self.lvl,
            map_block=self.map_block.name,
            body=[
                Position2(segment.x, segment.z)
                for segment in self.body
            ],
            direction=Vector2(self.direction.x, self.direction.z),
        )

    def __copy__(self) -> "Player":
        """Creates a copy of the player, including every snake segment."""
        player = super().__copy__()
        player.direction = Vector2(self.direction.x, self.direction.z)
        player.next_direction = Vector2(
            self.next_direction.x,
            self.next_direction.z
        )
        player.body = [
            Position2(segment.x, segment.z)
            for segment in self.body
        ]
        player.last_game_tick = self.last_game_tick
        return player
