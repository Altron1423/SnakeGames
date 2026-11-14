from dataclasses import dataclass

from libs.math import Position2, Vector2


@dataclass
class EntityToClientDTO:
    """Data Transfer Object for entity information sent to the client.

    Attributes:
        name (str): Name of the entity.
        id (int): Unique identifier of the entity.
        position (Position2): Current position of the entity.
        orientation (Vector2): Orientation vector of the entity.
        visual_action (str): Current visual action or animation state.
    """
    name: str
    id: int
    position: Position2
    orientation: Vector2
    visual_action: str
