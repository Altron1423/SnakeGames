from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class CreateSavesDTO:
    """Data Transfer Object for creating new saves.

    Attributes:
        name (str): Name of the save.
        version (list[int]): Version identifier.
    """
    name: str
    version: list[int]


@dataclass
class PresentationSaveDTO:
    """Data Transfer Object for displaying save information.

    Attributes:
        name (str): Name of the save.
        version (list[int]): Version identifier.
        last_open (datetime): Timestamp of last access.
        description (str): Description of the save.
    """
    name: str
    version: list[int]
    last_open: datetime
    description: str


@dataclass
class DataSaveDTO:
    """Data Transfer Object for save data content.

    Attributes:
        name (str): Name of the save.
        version (list[int]): Version identifier.
        description (str): Description of the save.
        last_open (datetime): Timestamp of last access.
        created (bool): Whether it's a newly created save.
    """
    name: str
    version: list[int]
    description: str
    last_open: datetime
    created: bool


@dataclass
class CreateSaveWF_DTO:
    """Data Transfer Object for save creation workflow.

    Attributes:
        name (str): Name of the save.
        version (list[int]): Version identifier.
        last_open (datetime): Timestamp of last access.
        description (str): Description of the save.
        path_to_save (Path): Path where the save is stored.
        created (bool): Whether it's a newly created save.
    """
    name: str
    version: list[int]
    last_open: datetime
    description: str
    path_to_save: Path
