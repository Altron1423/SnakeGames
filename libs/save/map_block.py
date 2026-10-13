from libs.save.map_chunk import MapChunk
from libs.math import Size2, Position2
from libs.dtos.entity import EntityToClientDTO

class MapBlock:
    """Represents a map block containing chunks and entities.

    Attributes:
        id (int): Unique identifier for the map block.
        size (Size2): The dimensions of the map block.
        size_coordinate (Size2): The size in pixels/coordinates.
        position (Position2): The position of the map block.
        name (str): The name of the map block.
        form (list[list[MapChunk | None]]): The matrix of chunks.
        players_in_game (list["Player"]): List of players in this block.
        players (dict[str, "Player"]): Dictionary of players by name.
        enemies (list["Enemy"]): List of enemies in this block.
        entities_dto (list[EntityToClientDTO]): DTOs for entities.
        entities_ranges (dict[tuple[str, str], int]): Distances between entities.
    """
    id: int = 1

    size: Size2
    size_coordinate: Size2
    position: Position2
    name: str
    form: list[
        list[
            MapChunk | None
        ]
    ]
    players_in_game: list["Player"]
    players: dict[str, "Player"]
    enemies: list["Enemy"]
    entities_dto: list[EntityToClientDTO]
    entities_ranges: dict[tuple[str, str], int]

    def __init__(self, size: Size2, name: str):
        """Initializes a new MapBlock instance.

        Args:
            size (Size2): The size of the block.
            name (str): The name of the block.
        """
        self.size = size
        self.size_coordinate = size * 50 * 16
        self.name = name
        self.position = Position2()
        self.id = 0
        self.form = []
        for z in range(size.z):
            self.form.append([None] * size.x)
        self.players_in_game = []
        self.players = {}
        self.enemies = []
        self.entities_dto = []
        self.entities_ranges = {}

    def set_form(self, form: list[list[MapChunk | None]]):
        """Sets the chunk matrix for the map block.

        Args:
            form (list[list[MapChunk | None]]): The new chunk matrix.
        """
        for z in range(self.size.z):
            for x in range(self.size.x):
                self.form[z][x] = form[z][x]

    def set_chunk_on(
            self,
            chunk: MapChunk | None,
            position: Position2
    ) -> None:
        """Sets a chunk at a specific position within the block.

        Args:
            chunk (MapChunk | None): The chunk to set.
            position (Position2): The position within the block.
        """
        if position in self.size:
            self.form[position.z][position.x] = chunk

    def get_chunk(
            self,
            position: Position2,
    ) -> MapChunk:
        """Gets the chunk at the specified position.

        Args:
            position (Position2): The position to get the chunk for.

        Returns:
            MapChunk: The chunk at the specified position.

        Raises:
            ValueError: If the position is not within the block's size.
        """
        if position in self.size:
            return self.form[position.z][position.x]
        raise ValueError(f"{position} not in {self.size}")

    def update(self):
        """Updates the data for all entities in the block.

        If no players are in the block, no updates are performed.
        """
        if len(self.players_in_game) == 0:
            return

        self.entities_dto = []
        self.entities_ranges = {}
        for player in self.players_in_game:
            self.entities_dto.append(
                player.get_light_data()
            )
        for enemy in self.enemies:
            self.entities_dto.append(
                enemy.get_light_data()
            )

        for entity_1 in self.entities_dto:
            for entity_2 in self.entities_dto:
                if entity_1 == entity_2:
                    continue
                elif (entity_2.name, entity_1.name) in self.entities_ranges:
                    continue
                x1, z1 = entity_1.position
                x2, z2 = entity_2.position
                self.entities_ranges[(entity_1.name, entity_2.name)] = abs(x1 - x2) + abs(z1 - z2)

    def get_near_entity(
            self, name: str, max_range: int
    ) -> dict[str, int]:
        """Returns a dictionary of entities within a certain range of a given name.

        Args:
            name (str): The name of the entity to check proximity to.
            max_range (int): The maximum distance.

        Returns:
            dict[str, int]: A dictionary where keys are entity names and values are distances.
        """
        entities_ranges = {}
        # max_range *= max_range
        for pair in self.entities_ranges:
            if name in pair:
                if self.entities_ranges[pair] <= max_range:
                    if pair[0] == name:
                        second_name = pair[1]
                    else:
                        second_name = pair[0]
                    entities_ranges[second_name] = self.entities_ranges[pair]
        return entities_ranges

    def get_entity_dto(self):
        """Returns the list of entity DTOs.

        Returns:
            list[EntityToClientDTO]: The list of entity DTOs.
        """
        return self.entities_dto

    def add_enemy(self, enemy: "Enemy"):
        """Adds an enemy to the block.

        Args:
            enemy ("Enemy"): The enemy instance to add.
        """
        enemy.map_block = self
        self.enemies.append(enemy)

    @property
    def Size(self):
        """Size2: The size of the map block."""
        return self.size

    @Size.setter
    def Size(self, size: Size2):
        """Sets the size of the map block."""
        self.size = size
        self.size_coordinate = size * 50

    @property
    def Name(self):
        """str: The name of the map block."""
        return self.name

    def __str__(self) -> str:
        """Returns a string representation of the block.

        Returns:
            str: The string representation.
        """
        return f"<{self.name}({self.id})>"

    def __copy__(self) -> "MapBlock":
        """Creates a copy of the MapBlock.

        Returns:
            MapBlock: The copy of the MapBlock.
        """
        map_block = MapBlock(self.size, self.name)
        map_block.id = MapBlock.id
        MapBlock.id += 1
        map_block.__set_clone_form__(self.form)
        return map_block

    def __set_clone_form__(self, form: list[list[MapChunk | None]]) -> None:
        """Internal method to copy the chunk matrix.

        Args:
            form (list[list[MapChunk | None]]): The matrix to copy from.
        """
        for x, z in self.size:
            if form[z][x] is not None:
                self.form[z][x] = form[z][x].__copy__()
