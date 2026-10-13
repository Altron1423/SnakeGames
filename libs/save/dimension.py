from . import BlockNotInDimensionException
from .map_block import MapBlock
from .map_chunk import MapChunk
from libs.math import Position2, Size2

class Dimension:
    """Represents a dimension in the game world.

    Attributes:
        id (int): Unique identifier for the dimension.
        size (Size2): The dimensions of the map (width and height).
        name (str): The name of the dimension.
        map_matrix (list[list[MapChunk | None]]): A 2D matrix representing the map chunks.
        blocks (list[MapBlock]): A list of all blocks present in this dimension.
        using_blocks (list[str]): A list of block names that are allowed in this dimension.
    """
    id: int = 0

    size: Size2
    name: str
    map_matrix: list[list[MapChunk | None]]
    blocks: list[MapBlock]
    using_blocks: list[str]

    def __init__(self, size: Size2, name: str) -> None:
        """Initializes a new Dimension instance.

        Args:
            size (Size2): The size of the dimension.
            name (str): The name of the dimension.
        """
        self.size = size
        self.name = name
        self.map_matrix = []

        for _ in range(size.z):
            self.map_matrix.append([None] * size.x)

        self.blocks = []
        self.using_blocks = []

    def add_map_block(
            self,
            map_block: MapBlock,
            position: Position2 = None
    ) -> bool:
        """Adds a map block to the dimension at a specified position.

        Args:
            map_block (MapBlock): The block to add.
            position (Position2, optional): The position to add the block. 
                Defaults to the block's own position if None.

        Returns:
            bool: True if the block was added successfully, False otherwise.

        Raises:
            BlockNotInDimensionException: If the block type is not allowed in this dimension.
        """
        if position is None:
            position = map_block.position
        else:
            map_block.position = position

        if map_block.name not in self.using_blocks:
            raise BlockNotInDimensionException(f"Блок <{map_block.name}>, не может существовать в <{self.name}>.")
        if not self.test_block_on_matrix(position, map_block):
            return False

        # map_block.generate_chunks()
        self.__set_block__(map_block, position)
        return True

    def add_using_block(self, map_block: str) -> None:
        """Adds a block type to the list of allowed blocks for this dimension.

        Args:
            map_block (str): The name of the block to allow.
        """
        self.using_blocks.append(map_block)

    def test_block_on_matrix(
            self,
            position: Position2,
            map_block: MapBlock
    ) -> bool:
        """Checks if a block can be placed at the given position.

        Args:
            position (Position2): The position to check.
            map_block (MapBlock): The block to test.

        Returns:
            bool: True if the position is empty, False otherwise.
        """
        for x, z in position + map_block.size:
            if self.map_matrix[x][z] is not None:
                return False
        return True

    def get_chunk(self, position: Position2) -> MapChunk:
        """Gets the chunk at the specified position.

        Args:
            position (Position2): The position to get the chunk for.

        Returns:
            MapChunk: The chunk at the specified position.
        """
        if position in self.size:
            return self.map_matrix[position.z][position.x]

    def update(self):
        """Updates all blocks in the dimension."""
        for i_blocks in self.blocks:
            i_blocks.update()

    @property
    def Name(self):
        """str: The name of the dimension."""
        return self.name

    def __set_block__(
            self,
            map_block: MapBlock,
            position: Position2 = None
    ) -> None:
        """Internal method to add a block to the dimension and update the matrix.

        Args:
            map_block (MapBlock): The block to add.
            position (Position2, optional): The position to add the block. Defaults to the block's position.
        """
        self.blocks.append(map_block)

        for xb, zb in map_block.size:
            d_pos = position + Position2(xb, zb)
            self.map_matrix[d_pos.z][d_pos.x] = map_block.form[zb][xb]

    def __str__(self) -> str:
        """Returns a string representation of the dimension.

        Returns:
            str: A string representation of the dimension.
        """
        return f"<{self.name}({self.id})>"

    def __copy__(self) -> "Dimension":
        """Creates a copy of the dimension.

        Returns:
            Dimension: A copy of the dimension.
        """
        dim = Dimension(self.size, self.name)
        dim.id = Dimension.id
        Dimension.id += 1
        dim.blocks = self.blocks.copy()
        dim.using_blocks = self.using_blocks.copy()
        dim.__fill_matrix_map__()
        return dim

    def __fill_matrix_map__(self) -> None :
        """Fills the map matrix with the blocks currently in the dimension."""
        for map_block in self.blocks:
            self.__set_block__(map_block)
