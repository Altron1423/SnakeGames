from dataclasses import dataclass


@dataclass
class DimensionSaveDTO:
    """Data Transfer Object for dimension save data.

    Attributes:
        full_name (str): Full path or name of the dimension save.
        name (str): Name of the dimension.
        blocks (list[str]): List of block identifiers in the dimension.
    """
    full_name: str
    name: str
    blocks: list[str]


@dataclass
class DimensionConfigDTO:
    """Data Transfer Object for dimension configuration.

    Attributes:
        name (str): Name of the dimension.
        size (str): Dimension size specification.
        blocks (list[str]): List of available blocks in the dimension.
    """
    name: str
    size: str
    blocks: list[str]
