from libs import loger, map_block_loader, MapBlock
from libs.generators import MapBlockGenerator
from libs.loaders.map_loader import MapLoader, map_loader
from libs.math import Position2
from libs.save.dimension import Dimension


class DimensionGeneratorTest:
    """A test class for testing dimension generation.

    Attributes:
        dimension (Dimension): The dimension object to be used for testing.
        map_loader (MapLoader): The loader used to load maps. Defaults to map_loader.
    """
    dimension: Dimension
    map_loader: MapLoader = map_loader

    def __init__(self, dimension: Dimension):
        """Initializes the DimensionGeneratorTest instance.

        Args:
            dimension (Dimension): The dimension object to be used for testing.
        """
        self.dimension = dimension

    def gen1(self) -> tuple[Position2, MapBlock] | None:
        """Generates a test dimension component.

        This method loads a test map block, generates a spawn position using
        MapBlockGenerator, and adds the block to the dimension.

        Returns:
            tuple[Position2, MapBlock] | None: A tuple containing the spawn position
                and the map block, or None if generation failed.
        """
        loger.log("gen1")
        st_block = map_block_loader.get_new("start_test_block")
        spawn_position = MapBlockGenerator.gen1(st_block)
        self.dimension.add_map_block(
            st_block,
            Position2(2, 3)
        )


        if spawn_position is not None:
            return spawn_position, st_block
        return None
