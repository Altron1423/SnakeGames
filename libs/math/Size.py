from libs.math import Vector2


class Size2(Vector2):
    """A 2D size class for representing dimensions.

    Attributes:
        _vector_type_ (str): Type identifier for the size.
    """
    _vector_type_ = "Size"

    def __post_init__(self):
        """Validates that x and z are positive."""
        if self.x < 0 or self.z < 0:
            raise TypeError("X and Z must be positive")

    def __contains__(self, item) -> bool:
        """Checks if a position is within the size.

        Args:
            item (Position2): The position to check.

        Returns:
            bool: True if the position is within the bounds, False otherwise.
        """
        from libs.math import Position2
        return 0 <= item.x <= self.x and 0 <= item.z <= self.z

    def __iter__(self):
        """Iterates over all Position2 points within the size.

        Yields:
            Position2: The next position in the grid.
        """
        from libs.math import Position2
        for z in range(self.z):
            for x in range(self.x):
                yield Position2(x, z)
