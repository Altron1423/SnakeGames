from libs import dimension_loader, SaveFull
from libs.generators import DimensionGeneratorTest


class SaveCreateTest:
    """A class for testing save creation.

    This class provides methods to create a test save with pre-defined data.
    """

    @staticmethod
    def create(save: SaveFull):
        """Creates a test save.

        This method loads a new dimension, adds it to the save, and uses
        DimensionGeneratorTest to generate some data for the save.

        Args:
            save (SaveFull): The save object to be populated.
        """
        dim = dimension_loader.get_new("start_test_dim")
        save.dimensions.append(dim)
        dim_gen = DimensionGeneratorTest(dim)
        data = dim_gen.gen1()
        if data is not None:
            save.spawn_position, save.spawn_map_block = data
        save.created = True
