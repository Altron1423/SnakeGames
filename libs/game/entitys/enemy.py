from .entity import Entity


class Enemy(Entity):
    """Represents an enemy in the game.

    Inherits from the Entity class.
    """
    entity_type: str = "Enemy"
    ...
