from dataclasses import dataclass


@dataclass
class MapPlateSaveDTO:
    """Data Transfer Object for map plate save data.

    Attributes:
        full_name (str): Full path or name of the map plate.
        name (str): Name of the map plate.
        id (int): Unique identifier of the map plate.
        type (str): Type of the map plate.
        custom_data (dict[str, str]): Custom data associated with the plate.
    """
    full_name: str
    name: str
    id: int
    type: str
    custom_data: dict[str, str]


@dataclass
class MapPlateConfigDTO:
    """Data Transfer Object for map plate configuration.

    Attributes:
        name (str): Name of the map plate.
        type (str): Type of the map plate.
        color (list[int]): Color of the map plate (RGBA).
        texture (str): Texture identifier.
        layer (int): Rendering layer.
        changeable (bool): Whether the plate can be changed.
    """
    name: str
    type: str
    color: list[int]
    texture: str
    layer: int
    changeable: bool
