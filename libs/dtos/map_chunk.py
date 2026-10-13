from dataclasses import dataclass


@dataclass
class MapChunkSaveDTO:
    """Data Transfer Object for map chunk save data.

    Attributes:
        full_name (str): Full path or name of the map chunk.
        name (str): Name of the map chunk.
        id (int): Unique identifier of the map chunk.
        changes_plates (dict[str, str]): Changes in plates.
    """
    full_name: str
    name: str
    id: int
    changes_plates: dict[str, str]


@dataclass
class MapChunkConfigDTO:
    """Data Transfer Object for map chunk configuration.

    Attributes:
        name (str): Name of the map chunk.
        size (str): Size of the map chunk.
        plates (dict[str, str]): Plate configuration.
        map_plates (list[list[str | int]]): Mapping of plates.
        height_map (list[list[int]]): Height map of the chunk.
    """
    name: str
    size: str
    plates: dict[str, str]
    map_plates: list[list[str | int]]
    height_map: list[list[int]]
