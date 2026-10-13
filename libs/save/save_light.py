import json
from libs.dtos.save import (
    DataSaveDTO
)
# from libs.file_works.saves import SavesWF
from pathlib import Path
from datetime import datetime


class SaveLight:
    """A lightweight save containing basic metadata.

    Attributes:
        path_save (Path): The path to the save file.
        name (str): The name of the save.
        version (list[int]): The version of the save.
        last_open (datetime): The last time the save was opened.
        description (str): A description of the save.
        created (bool): Whether the save has been created.
    """
    path_save: Path
    name: str
    version: list[int]
    last_open: datetime
    description: str
    created: bool

    def __init__(self, path):
        """Initializes a new SaveLight instance.

        Args:
            path (Path): The path to the save file.
        """
        self.path_save = path

    def fast_load(self):
        """Performs a fast load of the light save data.
        """
        from libs.file_works.saves import SavesWF

        SavesWF.load_save_light(self)


    def delete(self):
        """Deletes the save file.
        """
        from libs.file_works.saves import SavesWF
        SavesWF.delete(self.path_save)
