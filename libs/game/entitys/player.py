from libs import PLATE_SIZE, EntityToClientDTO
from libs.dtos import (
    ClientPlayerDTO,
    GameDataToServerDTO,
    GameDataToClientDTO,
    PlayerLoadDTO,
)
from libs.math import Position2, Vector2
from .entity import Entity
from .snake_segment import SnakeSegment


class Player(Entity):
    """Server-side snake head and owner of its body segments."""

    entity_type: str = "Player"
    was_selected: bool = False
    free_moving: bool = False
    last_game_tick: int = 0
    last_input_game_tick: int = -1

    body: list[SnakeSegment]

    INITIAL_LENGTH = 3

    def __init__(self):
        super().__init__()
        self.speed = PLATE_SIZE
        self.orientation = Vector2(1, 0)
        self.body = []
        self.last_game_tick = 0
        self.last_input_game_tick = -1
        self.was_selected = False

    def _create_segment(
        self,
        position: Position2,
        orientation: Vector2,
    ) -> SnakeSegment:
        """Creates a body entity attached to this player's map block."""
        segment = SnakeSegment(position, orientation)
        segment.map_block = self.map_block
        if self.name is not None:
            segment.name = f"{self.name}_segment_{segment.id}"
        return segment

    def set_default(self, name: str, spawn_position: Position2):
        """Initializes the head and creates the remaining starting segments."""
        self.name = name
        self.position = spawn_position.copy()
        self.orientation = Vector2(1, 0)
        self.was_selected = False
        self.last_game_tick = 0
        self.last_input_game_tick = -1

        self.body = [
            self._create_segment(
                Position2(
                    self.position.x - self.orientation.x * self.speed * index,
                    self.position.z - self.orientation.z * self.speed * index,
                ),
                self.orientation,
            )
            for index in range(1, self.INITIAL_LENGTH)
        ]

    def set_changes_from_client(
        self,
        dto: GameDataToServerDTO,
        game_tick: int | None = None,
    ):
        """Accepts at most one cardinal direction change during a game tick."""
        if game_tick is not None and game_tick != self.last_input_game_tick:
            self.was_selected = False
            self.last_input_game_tick = game_tick

        if dto.action != "select" or self.was_selected:
            return

        requested = dto.move
        is_cardinal = (
            (requested.x in (-1, 1) and requested.z == 0)
            or (requested.z in (-1, 1) and requested.x == 0)
        )
        if not is_cardinal:
            return

        # A snake cannot reverse directly into its own neck.
        if self.orientation == requested * -1:
            return

        # The DTO vector is not mutated or reused by the caller.
        self.orientation = requested
        self.was_selected = True

    def update(self, game_tick: int):
        """Moves the head once and makes each segment follow its predecessor."""
        if self.last_game_tick == game_tick:
            return

        self.last_game_tick = game_tick

        next_position = self.position + self.orientation * self.speed

        # The tail leaves its current cell during this move, so that cell is free.
        if any(
            next_position == segment.position
            for segment in self.body[:-1]
        ):
            return

        previous_head_position = self.position.copy()
        previous_body_positions = [
            segment.position for segment in self.body
        ]
        previous_tail_orientation = (
            self.body[-1].orientation.copy()
            if self.body
            else self.orientation.copy()
        )

        move_result, collected_fruit = self.__move_plate__()
        if move_result < 0:
            return

        for index, segment in enumerate(self.body):
            old_segment_position = previous_body_positions[index]
            new_segment_position = (
                previous_head_position
                if index == 0
                else previous_body_positions[index - 1]
            )

            segment.position = new_segment_position.copy()
            segment.orientation = Vector2(
                int((new_segment_position.x - old_segment_position.x) / self.speed),
                int((new_segment_position.z - old_segment_position.z) / self.speed),
            )

        if move_result == 1 and collected_fruit is not None:
            self.add_xp(collected_fruit.scored)

            # Remove the fruit after the head has entered its cell.
            _, fruit_plate, _ = self.__get_info_positon__(self.position)
            if collected_fruit in fruit_plate.entities:
                fruit_plate.entities.remove(collected_fruit)

            # The new tail occupies the cell the old tail just left.
            new_tail_position = (
                previous_body_positions[-1]
                if previous_body_positions
                else previous_head_position
            )
            self.body.append(
                self._create_segment(
                    new_tail_position,
                    previous_tail_orientation,
                )
            )

    def get_data_for_client(self, game_tick) -> GameDataToClientDTO:
        """Builds the full state sent to this player's client."""
        return GameDataToClientDTO(
            game_tick=game_tick,
            map_block="",
            entities=self.map_block.get_entity_dto(),
            player=self.__player_data__,
            chunk_position=Position2(0, 0),
            position=self.position,
        )

    def get_light_data(self) -> EntityToClientDTO:
        """Provides this player and its segment entities to other clients."""
        return EntityToClientDTO(
            name=self.name,
            id=self.id,
            position=self.position,
            orientation=self.orientation,
            visual_action="walk",
            body=[segment.get_light_data() for segment in self.body],
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
        """Loads the player's progression settings."""
        return super().load_from_config(dto)

    @property
    def __player_data__(self) -> ClientPlayerDTO:
        """Prepares the local player's state and segment entities for the client."""
        return ClientPlayerDTO(
            name=self.name,
            id=self.id,
            position=self.position,
            orientation=self.orientation,
            xp=self.xp,
            lvl=self.lvl,
            map_block=self.map_block.name,
            body=[segment.get_light_data() for segment in self.body],
        )

    def __copy__(self) -> "Player":
        """Creates a player copy with independent body segment entities."""
        player: Player = super().__copy__()
        player.position = self.position.copy()
        player.orientation = self.orientation.copy()
        player.map_block = self.map_block
        player.speed = self.speed
        player.was_selected = self.was_selected
        player.last_game_tick = self.last_game_tick
        player.last_input_game_tick = self.last_input_game_tick
        player.body = [segment.__copy__() for segment in self.body]
        return player
