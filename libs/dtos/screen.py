from dataclasses import dataclass
from libs.math import Recalc, Vector2


@dataclass
class ButtonDTO:
    """Data Transfer Object for button configuration.

    Attributes:
        type (str): Type of the button.
        polygons_name (str): Name of the polygon used for the button.
        position (Recalc | None): Recalculated position. Defaults to None.
        size (Recalc | None): Recalculated size. Defaults to None.
        text (str | None): Text displayed on the button. Defaults to None.
        triggers (dict[tuple[str, bool], str] | None): Dictionary mapping key/event to action. Defaults to None.
        png_name (str | None): Name of the PNG image for the button. Defaults to None.
    """
    type: str
    polygons_name: str
    position: Recalc | None = None
    size: Recalc | None = None
    text: str | None = None
    triggers: dict[tuple[str, bool], str] | None = None
    png_name: str | None = None


@dataclass
class WindowDataDTO:
    """Data Transfer Object for window data.

    Attributes:
        recalc_position (Recalc): Recalculated position.
        recalc_size (Recalc): Recalculated size.
        default_polygonizer (str): Name of the default polygonizer.
        background (list[int] | None): Background color. Defaults to None.
        cord_new_button (list[int | float] | None): Coordinates for new buttons. Defaults to None.
    """
    recalc_position: Recalc
    recalc_size: Recalc
    default_polygonizer: str
    background: list[int] | None = None
    cord_new_button: list[int | float] | None = None


@dataclass
class WindowDTO:
    """Data Transfer Object for window configuration.

    Attributes:
        name (str): Name of the window.
        data (WindowDataDTO): Data associated with the window.
        buttons (list[ButtonDTO]): List of buttons in the window.
    """
    name: str
    data: WindowDataDTO
    buttons: list[ButtonDTO]
