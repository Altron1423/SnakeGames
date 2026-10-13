from libs.Loger import loger
from libs.math import Position2
from libs.save import (
    SaveLight, Dimension, MapBlock
)

class SaveFull(SaveLight):
    """A full save containing dimensions, map blocks, and other game data.

    Attributes:
        spawn_map_block (MapBlock): The block where the player spawns.
        spawn_position (Position2): The position where the player spawns.
        dimensions (list[Dimension]): A list of dimensions in the save.
    """
    spawn_map_block: MapBlock
    spawn_position: Position2
    dimensions: list[Dimension]

    def __init__(self, save_light: SaveLight):
        """Initializes a new SaveFull instance.

        Args:
            save_light (SaveLight): The light save data used for initialization.
        """
        super().__init__(save_light.path_save)

        from libs.file_works import SavesWF

        self.saves_wf = SavesWF
        self.fast_load()

        self.full_load()
        loger.status(f"SaveFull \"{self.name}\" loaded")

    def full_load(self):
        """Loads all the data for the full save.

        Sets the dimensions list and loads data from the save file.
        """
        self.dimensions = []
        if self.created:
            sw = self.saves_wf(self.path_save)
            sw.load_save_full(self)
            self.__load__()

    def need_created(self) -> bool:
        """Checks if the save needs to be created.

        Returns:
            bool: True if the save has not been created yet, False otherwise.
        """
        return self.created is False

    def saving(self):
        """Saves the full save data to the file system.

        """
        s_wf = self.saves_wf(self.path_save)
        s_wf.saving(self)

    def update(self):
        """Updates all dimensions in the save.

        """
        for i_dimension in self.dimensions:
            i_dimension.update()

    def __load__(self):
        """Internal method to load data from the file.
        """
        ...
