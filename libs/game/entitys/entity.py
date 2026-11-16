from __future__ import annotations

from libs import MapBlock, MapPlate, PLATE_SIZE, EntityToClientDTO
from libs.game.sub_classes import ProgressBar
from libs.game.sub_classes.progress_bar import TriggersDTO
from libs.math import Position2, Vector2

def get_sign(x: int | float) -> int:
    """Determines the sign of a number.

    Args:
        x (int | float): The number to check.

    Returns:
        int: 1 if x > 0, -1 if x < 0, and 0 otherwise.
    """
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0

FIX_CORRECT_DOT = 3

class Entity:
    """Base class for all entities in the game.

    Contains common properties and behaviors for any entity, such as position,
    health, mana, and movement logic.
    """
    entity_type: str = "Entity"
    name: None | str
    id: int
    id_was_created: int = 0

    xp: ProgressBar
    raising_xp: float
    xp_boost: float
    lvl: int

    map_block: MapBlock | None = None
    position: Position2
    orientation: Vector2
    speed_control: float
    speed: float
    free_moving: bool = True

    collision: Vector2
    step_height: int

    def __init__(self):
        """Initializes a new Entity instance with default values."""
        self.name = None
        self.id = Entity.id_was_created
        Entity.id_was_created += 1

        self.xp = ProgressBar(unlimit=True)
        self.xp.set_triggers(TriggersDTO(
            _limit=self.__lvl_up__
        ))
        self.raising_xp = 1.05
        self.xp_boost = 1
        self.lvl = 1

        self.position = Position2()
        self.orientation = Vector2(0, 0)
        self.speed_control = 1
        self.speed = 8

        collision = 46
        self.collision = Vector2(collision // 2, collision // 2)
        self.step_height = 10

    def add_xp(self, xp: int) -> None:
        """Adds experience points to the entity.

        Args:
            xp (int): The amount of experience to add (before boost).
        """
        self.xp += int(xp * self.xp_boost)

    def update(self):
        """Updates the entity's state, including attributes and movement."""
        self.__move__()

    def transition_to(self, map_block: MapBlock):
        """Transitions the entity to a new map block.

        Args:
            map_block (MapBlock): The target map block.
        """
        if self.map_block is not None:
            self.transition_from()
        self.map_block = map_block
        map_block.players_in_game.append(self)
        self.map_block.players[self.name] = self
        self.position = Position2(150, 150)

    def transition_from(self):
        """Removes the entity from the current map block."""
        self.map_block.players_in_game.remove(self)
        self.map_block.players.pop(self.name)

    def get_light_data(self) -> EntityToClientDTO:
        """Retrieves data for light calculation.

        Returns:
            EntityToClientDTO: The DTO containing entity light data.
        """
        return EntityToClientDTO(
            self.name,
            self.id,
            self.position,
            self.orientation,
            "idle"
        )

    @classmethod
    def load_from_config(cls, dto) -> "Entity":
        """Loads an entity from a provided configuration DTO.

        Args:
            dto: The DTO containing entity configuration.

        Returns:
            Entity: The loaded entity instance.
        """
        entity = cls()
        entity.race = dto.race
        entity.xp.set_limit(dto.to_first_lvlup)
        entity.raising_xp = dto.raising_xp
        entity.xp_boost = dto.xp_boost
        return entity


    def __move__(self):
        """Handles entity movement and collision detection."""
        if self.free_moving:
            self.__move_free__()

    def __move_plate__(self) -> tuple[int, Entity | None]:
        """Moves the entity by one plate and reports a collected fruit."""
        move_on = self.orientation * self.speed
        _, _, start_height = self.__get_info_positon__(self.position)
        new_position = self.position + move_on

        # Check map bounds before asking the map for the destination plate.
        if new_position not in self.map_block.size_coordinate:
            return -1, None

        _, new_plate, new_height = self.__get_info_positon__(new_position)
        if abs(new_height - start_height) > self.step_height:
            return -1, None

        collected_fruit = None
        for entity in new_plate.entities:
            if entity.entity_type == "Player":
                return -1, None
            if entity.entity_type == "Fruit":
                collected_fruit = entity
                break

        # The entity must enter the fruit's cell before the caller handles it.
        self.position = new_position
        if collected_fruit is not None:
            return 1, collected_fruit
        return 0, None


    def __move_free__(self):
        """Свободно движение без привязки к сетке клеток"""
        move_on = self.orientation * self.speed * self.speed_control
        _, start_plate, start_heigh = self.__get_info_positon__(self.position)
        for i in (Vector2(1, 0), Vector2(0, 1)):
            move_on_1d: Vector2 = move_on * i
            if move_on_1d.x != 0:
                collision = self.collision * i * get_sign(move_on_1d.x)
                correct_dots = (Vector2(0, self.collision.z-FIX_CORRECT_DOT), Vector2(0, -self.collision.z+FIX_CORRECT_DOT))
            elif move_on_1d.z != 0:
                collision = self.collision * i * get_sign(move_on_1d.z)
                correct_dots = (Vector2(self.collision.x-FIX_CORRECT_DOT, 0), Vector2(-self.collision.x+FIX_CORRECT_DOT, 0))
            else:
                continue
            new_position = self.position + move_on_1d + collision
            if not new_position in self.map_block.size_coordinate:
                continue

            for correct_dot in correct_dots:
                position_plate, new_plate, new_heigh = self.__get_info_positon__(new_position + correct_dot)
                position_plate += 1
                if move_on_1d.x < 0 or move_on_1d.z < 0:
                    position_plate += 72

                if abs(new_heigh - start_heigh) > self.step_height:
                    move_on_1d = (position_plate - self.position)*i
                    if move_on_1d.x > 0 or move_on_1d.z > 0:
                        move_on_1d -= collision
                    break
            self.position += move_on_1d

    def __get_info_positon__(self, pos: Position2 = None) -> tuple[Position2 | Vector2, MapPlate, int]:
        """Helper method to get position info relative to the map structure.

        Args:
            pos (Position2, optional): The position to check. Defaults to self.position.

        Returns:
            tuple[Position2, MapPlate, int]: A tuple containing the position in plate, 
                                            the plate itself, and the height.
        """
        if pos is None:
            pos = self.position
        plate_position, map_plate, height = self.map_block.get_info_positon(pos)
        return plate_position * PLATE_SIZE, map_plate, height

    def __lvl_up__(self) -> None:
        """Handles the level up process when enough XP is gathered."""
        quantity, max_xp = self.xp.get_full(True)
        quantity -= max_xp
        max_xp = int(max_xp * self.raising_xp)
        self.xp.update(quantity, max_xp)
        self.lvl += 1

    def __copy__(self):
        """Creates a copy of the current entity.

        Returns:
            Entity: A copy of the entity.
        """
        to = self.__class__()
        to.name = self.name
        to.xp = self.xp.__copy__()
        to.raising_xp = self.raising_xp
        to.lvl = self.lvl
        to.position = self.position
        to.orientation = self.orientation
        to.speed = self.speed

        return to
