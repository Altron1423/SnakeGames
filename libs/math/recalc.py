from libs.math import Size2, Position2, Vector2


class Recalc:
    """A class for performing recalculations of positions.

    Attributes:
        k (Vector2): Scale factor.
        b (Vector2): Bias/offset.
        _type_ (str): Type identifier.
    """
    k: Vector2
    b: Vector2
    _type_: str = "Recalc"

    def __init__(self, k: Vector2 = None, b: Vector2 = None):
        """Initializes the Recalc instance.

        Args:
            k (Vector2 | None): Scale factor. Defaults to a zero Vector2.
            b (Vector2 | None): Bias/offset. Defaults to a zero Position2.
        """
        if k is None:
            k = Vector2()
        if b is None:
            b = Position2()
        self.k = k
        self.b = b

    @classmethod
    def load_from_str(cls, raw_data: str) -> "Recalc":
        """Parses a Recalc object from a string.

        Args:
            raw_data (str): String in the format "<Recalc:k_x,k_z/b_x,b_z>".

        Returns:
            Recalc: A new Recalc instance.

        Raises:
            TypeError: If the string format or type is incorrect.
        """
        if raw_data[0] == '<' and raw_data[-1] == '>':
            data = raw_data[1:-1]
            tp, data = data.split(':', maxsplit=1)
            if tp != cls._type_:
                raise TypeError(f"{raw_data} string not {cls._type_}")
            return cls(*[Vector2(vec) for vec in data.split('/')])
        else:
            raise TypeError(f"{raw_data} only accepts strings for {cls._type_}")

    def value(self, size: Size2 | Position2) -> Position2:
        """Calculates the value based on scale and bias.

        Args:
            size (Size2 | Position2): The base position or size.

        Returns:
            Position2: The calculated position.
        """
        return size * self.k + self.b

    def __add__(self, other):
        """Adds another object to this Recalc instance.

        Args:
            other (Position2 | Size2 | Vector2): Object to add.

        Returns:
            Recalc: The updated Recalc instance.
        """
        if isinstance(other, (Position2, Size2)):
            self.b += other
        elif isinstance(other, Vector2):
            self.k += other

        return self

    def __str__(self) -> str:
        """Returns the string representation of the Recalc instance.

        Returns:
            str: String in the format "<Recalc:k/b>".
        """
        return f"<{self._type_}:{self.k}/{self.b}>"

    @staticmethod
    def default() -> "Recalc":
        """Returns a default Recalc instance.

        Returns:
            Recalc: A Recalc instance with zero scale and (10, 10) bias.
        """
        return Recalc(Vector2(), Vector2(10, 10))

    @staticmethod
    def default_very_faraway() -> "Recalc":
        """Returns a Recalc instance with extreme bias.

        Returns:
            Recalc: A Recalc instance with (10, 10) scale and (-1000, -1000) bias.
        """
        return Recalc(Vector2(10, 10), Vector2(-1000, -1000))
