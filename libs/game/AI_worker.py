from pathlib import Path
from typing import Callable

from ..file_works.compilator import Compilator
from libs.math import Vector2, Position2
from .. import MapBlock, MapPlate, PLATE_SIZE
from .entitys import ClientPlayer

class PositionData:
    plate: MapPlate
    height: int

    def __init__(self, plate: MapPlate, height: int):
        self.plate = plate
        self.height = height

    def __eq__(self, other: int) -> bool:
        if other == 1:
            return self.plate.name == "test_plate1"
        elif other == 2:
            return self.plate.name == "test_plate2"
        elif other == 3:
            for entity in self.plate.entities:
                if entity.entity_type == "Fruit":
                    return True
            return False
        return False

    def __str__(self) -> str:
        return f"<DataOf_{self.plate.name}>"


class Snake:
    player: ClientPlayer
    action: str
    rd: dict = {
        'right': 1,
        'left': 3,
        'down': 2,
        'up': 0,
    }
    rotate_transformation: list = [
        lambda x, y: (x, -y),
        lambda x, y: (y, x),
        lambda x, y: (-x, y),
        lambda x, y: (-y, -x),
    ]
    rotate_int: int

    def __init__(self, player: ClientPlayer) -> None:
        self.player = player
        self.action = "up"
        self.rotate_int = 2

    def Right(self):
        self.action = "right"

    def Left(self):
        self.action = "left"

    def apply(self):
        if self.action == "right":
            rotate = (1, 0)
        elif self.action == "left":
            rotate = (-1, 0)
        else:
            rotate = (0, 1)
        self.action = "up"
        rotate = Vector2(self.rotate_func(*rotate))
        self.player.orientation = rotate

    @property
    def rotate(self) -> int:
        return self.rd[self.player.direction_view]

    @property
    def rotate_func(self) -> Callable[[int, int], tuple[int, int]]:
        return self.rotate_transformation[self.rotate]


class Map:
    snake: Snake
    caching_position: dict[tuple[int, int], PositionData]

    def __init__(self, snake: Snake) -> None:
        self.snake = snake
        self.caching_position = {}

    def position_data(self, x, y):
        data = self.caching_position.get((x, y))
        if data is not None:
            return data
        p = Position2(
            self.rotate(x, y)
        )
        p += self.position // PLATE_SIZE
        try:
            pos, plate, height = self.map_block.get_info_positon(abs_plate_position=p)
            pd = PositionData(plate, height)
            self.caching_position[(x, y)] = pd
            return pd
        except ValueError:
            return None


    def PosInfo(self, x, y):
        return self.position_data(x, y)

    def clear(self):
        self.caching_position = {}

    @property
    def map_block(self) -> MapBlock:
        return self.snake.player.map_block

    @property
    def rotate(self) -> Callable[[int, int], tuple[int, int]]:
        return self.snake.rotate_func

    @property
    def position(self) -> Position2:
        return self.snake.player.position


class AIWorker:
    snake: Snake
    map: Map
    compilator: Compilator
    function: Callable

    def __init__(self, player: ClientPlayer):
        self.snake = Snake(player)
        self.map = Map(self.snake)
        self.compilator = Compilator(
            Path().cwd() / "python_compile_code.py"
        )
        self.compilator.compile(
            Path().cwd() / "psevdo_code.py"
        )
        self.function = self.compilator.load()

    def run(self):
        self.map.clear()
        self.function(self.snake, self.map)
        self.snake.apply()