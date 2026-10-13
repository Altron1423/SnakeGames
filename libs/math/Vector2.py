class Vector2:
    """A 2D vector class for mathematical operations.

    Attributes:
        x (int): X coordinate.
        z (int): Z coordinate.
        _len_ (float): Magnitude of the vector.
        _re_calc_ (bool): Flag to indicate if length needs recalculation.
        _vector_type_ (str): Type identifier for the vector.
    """
    x: int
    z: int
    _len_: float = 0
    _re_calc_: bool = False
    _vector_type_ = "Vector2"

    def __init__(self, *position):
        """Initializes the Vector2 instance.

        Args:
            *position: Variable arguments for coordinates.
                Can be (x, z), (x, z, y), or a string formatted as "<Vector2:x,z>".
        """
        if len(position) > 2:
            raise TypeError(f"{self._vector_type_} only accepts two positions")
        if len(position) == 1:
            if type(position[0]) == str:
                self.from_string(position[0])
            elif type(position[0]) in [tuple, list]:
                self.set(*position[0])
        else:
            self.set(*position)

        self.__post_init__()
        self.__re_len__()

    def set(self, *position):
        """Sets the x and z coordinates of the vector.

        Args:
            *position: Coordinate values.
        """
        if len(position) == 2:
            self.x = position[0]
            self.z = position[1]
        elif len(position) == 1:
            self.x = position[0]
            self.z = 0
        elif len(position) == 0:
            self.x = self.z = 0

    def from_string(self, raw_data: str):
        """Parses the vector from a string.

        Args:
            raw_data (str): String in the format "<Vector2:x,z>".

        Raises:
            TypeError: If the string format or type is incorrect.
        """
        if raw_data[0] == '<' and raw_data[-1] == '>':
            data = raw_data[1:-1]
            tp, data = data.split(':')
            if tp != self._vector_type_:
                print(data)
                raise TypeError(f"This string not {self._vector_type_}")
            try:
                self.set(*list(map(int, data.split(','))))
            except:
                self.set(*list(map(float, data.split(','))))
        else:
            raise TypeError(f"{raw_data} only accepts strings for {self._vector_type_}")

    def __post_init__(self):
        """Placeholder for post-initialization logic."""
        ...

    def __re_len__(self):
        """Recalculates the length of the vector if required."""
        if self._re_calc_:
            self._len_ = (self.x ** 2 + self.z ** 2) ** 0.5

    def __len__(self):
        """Returns the magnitude of the vector."""
        return self._len_

    def __mul__(self, other):
        """Multiplies the vector by a scalar.

        Args:
            other (int | float | Vector2): Scalar or another vector.

        Returns:
            Vector2: A new scaled vector.
        """
        v = self.__class__()

        if isinstance(other, int):
            v.set(self.x * other, self.z * other)
        elif isinstance(other, float):
            v.set(int(self.x * other), int(self.z * other))
        elif isinstance(other, (self.__class__, Vector2)):
            v.set(self.x * other.x, self.z * other.z)

        v.__re_len__()
        return v

    def __add__(self, other):
        """Adds another vector to this vector.

        Args:
            other (int | Vector2): Integer or another vector.

        Returns:
            Vector2: A new summed vector.
        """
        v = self.__class__()

        if isinstance(other, int):
            v.set(self.x + other, self.z + other)
        elif isinstance(other, self.__class__):
            v.set(self.x + other.x, self.z + other.z)
        elif isinstance(other, Vector2):
            v.set(self.x + other.x, self.z + other.z)

        v.__re_len__()
        return v

    def __sub__(self, other):
        """Subtracts another vector from this vector.

        Args:
            other (int | Vector2): Integer or another vector.

        Returns:
            Vector2: A new subtracted vector.
        """
        v = self.__class__()

        if isinstance(other, int):
            v.set(self.x - other, self.z - other)
        elif isinstance(other, self.__class__):
            v.set(self.x - other.x, self.z - other.z)
        elif isinstance(other, Vector2):
            v.set(self.x - other.x, self.z - other.z)

        v.__re_len__()
        return v

    def __mod__(self, other):
        """Performs modulo operation on the vector.

        Args:
            other (int | Vector2): Integer or another vector.

        Returns:
            Vector2: A new modulo vector.
        """
        v = self.__class__()

        if isinstance(other, int):
            v.set(self.x % other, self.z % other)
        elif isinstance(other, self.__class__):
            v.set(self.x % other.x, self.z % other.z)
        elif isinstance(other, Vector2):
            v.set(self.x % other.x, self.z % other.z)

        v.__re_len__()
        return v

    def __floordiv__(self, other):
        """Performs floor division on the vector.

        Args:
            other (int): Integer divisor.

        Returns:
            Vector2: A new vector with floor-divided components.
        """
        v = self.__class__()

        if isinstance(other, int):
            v.set(self.x // other, self.z // other)
        elif isinstance(other, self.__class__):
            v.set(self.x // other.x, self.z // other.z)

        v.__re_len__()
        return v

    def __truediv__(self, other):
        """Performs true division on the vector.

        Args:
            other (int | float | Vector2): Divisor.

        Returns:
            Vector2: A new divided vector.
        """
        v = self.__class__()

        if isinstance(other, (int, float)):
            v.set(self.x / other, self.z / other)
        elif isinstance(other, self.__class__):
            v.set(self.x / other.x, self.z / other.z)

        v.__re_len__()
        return v

    def __str__(self):
        """Returns the string representation of the vector.

        Returns:
            str: String in the format "<Vector2:x,z>".
        """
        return f"<{self._vector_type_}:{self.x},{self.z}>"

    def __eq__(self, other: Vector2) -> bool:
        """Checks equality between two vectors.

        Args:
            other (Vector2): The other vector to compare.

        Returns:
            bool: True if they are equal, False otherwise.
        """
        return self.x == other.x and self.z == other.z

    @property
    def tuple(self):
        """Returns the vector components as a tuple.

        Returns:
            tuple: (x, z)
        """
        return self.x, self.z


if __name__ == "__main__":
    v = Vector2(10, 20)
    print(v)
    print(v%3)
    print(v//3)
