from libs.math import Position2, Size2
from .map_plate import MapPlate

class MapChunk:
    """Represents a chunk of the map within a MapBlock.

    Attributes:
        id (int): Unique identifier for the chunk.
        name (str): The name of the chunk.
        position (Position2): The position of the chunk.
        size (Size2): The size of the chunk.
        map (list[list[MapPlate | None]]): The matrix of plates.
        height_map (list[list[int]]): A 2D matrix representing the height map.
    """
    id: int = 1

    name: str
    position: Position2
    size: Size2
    map: list[
        list[
            MapPlate | None
        ]
    ]
    height_map: list[
        list[
            int
        ]
    ]

    def __init__(self, name: str, size: Size2):
        """Initializes a new MapChunk instance.

        Args:
            name (str): The name of the chunk.
            size (Size2): The size of the chunk.
        """
        self.position = Position2()
        self.name = name
        self.size = size
        self.id = 0
        self.map = [
            [None] * self.size.x for _ in range(self.size.z)
        ]
        # self.height_map = [[None] * self.size.x for _ in range(self.size.z)]

    def set_plate_on(
            self,
            plate: MapPlate,
            position: Position2
    ) -> None:
        """Sets a plate at a specific position within the chunk.

        Args:
            plate (MapPlate): The plate to set.
            position (Position2): The position within the chunk.
        """
        if position in self.size:
            self.map[position.z][position.x] = plate

    @property
    def Name(self):
        """str: The name of the chunk.
        """
        return self.name

    def get_plate(
            self,
            position: Position2,
    ) -> MapPlate:
        """Gets the plate at the specified position.

        Args:
            position (Position2): The position to get the plate for.

        Returns:
            MapPlate: The plate at the specified position.

        Raises:
            ValueError: If the position is not within the chunk's size.
        """
        if position in self.size:
            return self.map[position.z][position.x]
        raise ValueError(f"{position} not in {self.size}")

    def get_height(
            self,
            position: Position2,
    ) -> int:
        """Gets the height at the specified position.

        Args:
            position (Position2): The position to get the height for.

        Returns:
            int: The height at the specified position.

        Raises:
            ValueError: If the position is not within the chunk's size.
        """
        if position in self.size:
            return self.height_map[position.z][position.x]
        raise ValueError(f"{position} not in {self.size}")

    def __str__(self) -> str:
        """Returns a string representation of the chunk.

        Returns:
            str: The string representation.
        """
        return f"<{self.name}({self.id})>"

    def __copy__(self) -> "MapChunk":
        """Creates a copy of the MapChunk.

        Returns:
            MapChunk: The copy of the MapChunk.
        """
        map_chunk = MapChunk(self.name, self.size)
        map_chunk.position = self.position + 0
        map_chunk.id = MapChunk.id
        MapChunk.id += 1
        map_chunk.height_map = self.height_map.copy() # This is a shallow copy of the outer list, need to be careful
        map_chunk.__set_clone_map__(self.map)
        return map_chunk

    def __set_clone_map__(self, map: list[list[MapPlate | None]]) -> None:
        """Internal method to copy the plate matrix.

        Args:
            map (list[list[MapPlate | None]]): The matrix to copy from.
        """
        for x, z in self.size:
            map_plate = map[z][x]
            if map_plate.changeable:
            # if map_plate is not None and hasattr(map_plate, 'changeable') and map_plate.changeable:
                map_plate = map_plate.__copy__()
            self.map[z][x] = map_plate
