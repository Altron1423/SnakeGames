from dataclasses import dataclass


@dataclass
class MapBlockSaveDTO:
    """Data Transfer Object for map block save data.

    Attributes:
        full_name (str): Full path or name of the map block.
        name (str): Name of the map block.
        id (int): Unique identifier of the map block.
        position (str): Position description of the map block.
        chunks (list[list[str | None]]): Data representing the chunks of the map block.
    """
    full_name: str
    name: str
    id: int
    position: str
    chunks: list[list[str | None]]


@dataclass
class MapBlockConfigDTO:
    """Data Transfer Object for map block configuration.

    Attributes:
        name (str): Name of the map block.
        size (str): Size specification of the map block.
        form (list[list[str | None]]): Representation of the map block form.
    """
    name: str
    size: str
    form: list[list[str | None]]
