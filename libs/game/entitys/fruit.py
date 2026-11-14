from .item import Item


class Fruit(Item):
    """Represents a fruit in the game.

    Inherits from the Item class.
    """
    entity_type: str = "Fruit"
    scored: int

    def __init__(self):
        """Initializes a new Player instance."""
        super().__init__()
        self.scored = 100
