from .Vector2 import Vector2


class Vector3:
    """A 3D vector class for mathematical operations.

    Attributes:
        x (int): X coordinate.
        y (int): Y coordinate.
        z (int): Z coordinate.
        _vector_type_ (str): Type identifier for the vector.
    """
    x: int
    y: int
    z: int
    _vector_type_ = "Vector3"

    def __init__(self, *position):
        """Initializes the Vector3 instance.

        Args:
            *position: Variable arguments for coordinates.
        """
        self.set(*position)

    def set(self, *position):
        """Sets the x, y, and z coordinates of the vector.

        Args:
            *position: Coordinate values.
        """
        position += [0] * (3 - len(position))
        self.x, self.y, self.z = position

    def __mul__(self, other):
        """Multiplies the vector by a scalar.

        Args:
            other (int): Scalar value.

        Returns:
            Vector3: A new scaled vector.
        """
        pos = Vector3()

        if isinstance(other, int):
            pos.set(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vector3):
            pos.set(self.x * other.x, self.y, self.z * other.z)

        return pos

    def __add__(self, other):
        """Adds another vector to this vector.

        Args:
            other (int | Vector3 | Vector2): Integer or another vector.

        Returns:
            Vector3: A new summed vector.
        """
        pos = Vector3()

        if isinstance(other, int):
            pos.set(self.x + other, self.y + other, self.z + other)
        elif isinstance(other, Vector3):
            pos.set(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, Vector2):
            pos.set(self.x + other.x, self.y, self.z + other.z)

        return pos
