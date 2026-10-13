from libs.math import Position2

class MapPlate:
    """Represents a plate in a map chunk.

    Attributes:
        id (int): Unique identifier for the plate.
        name (str): The name of the plate.
        type (str): The type of the plate.
        position (Position2): The position of the plate.
        color (list[int]): The color of the plate (RGBA).
        texture (str | None): The texture of the plate.
        layer (int): The layer of the plate.
        changeable (bool): Whether the plate can be changed.
        entities (list): A list of entities on this plate.
    """
    id = 1

    name: str
    type: str
    position: Position2
    color: list[int]
    texture: str | None
    layer: int
    changeable: bool
    entities: list

    def __init__(self, name_plate: str):
        """Initializes a new MapPlate instance.

        Args:
            name_plate (str): The name of the plate.
        """
        self.position = Position2()
        self.name = name_plate
        self.id = 0
        self.entities = []
        self.changeable = False

    def get_custom_data(self) -> dict:
        """Returns custom data associated with the plate.

        Returns:
            dict:
        """
        return {}

    @property
    def Name(self):
        """str: The name of the plate.
        """
        return self.name

    def __str__(self) -> str:
        """Returns a string representation of the plate.

        Returns:
            str: The string representation.
        """
        return f"<{self.name}({self.id})>"

    def __copy__(self) -> "MapPlate":
        """Creates a copy of the MapPlate.

        Returns:
            MapPlate: The copy of the MapPlate.
        """
        map_plate = MapPlate(self.name)
        map_plate.position = self.position + 0
        map_plate.id = MapPlate.id
        MapPlate.id += 1
        map_plate.type = self.type
        map_plate.changeable = self.changeable
        map_plate.color = self.color.copy()
        map_plate.texture = self.texture
        map_plate.layer = self.layer

        return map_plate
