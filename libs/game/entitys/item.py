from .entity import Entity


class Item(Entity):
    """Represents an item in the game.

    Inherits from the Entity class.
    """
    entity_type: str = "Item"
    ...
