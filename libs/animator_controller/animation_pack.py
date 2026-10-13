from random import randint
import pygame as pg
from libs.math import Size2


class AnimationPack:
    """A collection of surfaces representing an animation.

    Attributes:
        size (Size2): The size of each animation frame.
        surfaces (list[pg.Surface]): The list of surfaces in the animation.
        count (int): Number of frames in the animation.
        time_to_surface (int): The number of ticks between each frame.
        _animation_seed (int): Seed for choosing the starting frame.
    """

    size: Size2
    surfaces: list[pg.Surface]
    count: int
    time_to_surface: int
    _animation_seed: int

    def __init__(self):
        """Initializes an empty AnimationPack with default values."""
        self.size = Size2()
        self.surfaces = []
        self.count = 0
        self._animation_seed = 0
        self.time_to_surface = 10

    def get_surface(self, tick: int = 0) -> pg.Surface:
        """Retrieves the current surface for a given tick.

        Args:
            tick (int): The current tick count. Defaults to 0.

        Returns:
            pg.Surface: The surface to be displayed for the given tick.
        """
        return self.surfaces[(tick + self._animation_seed) // self.time_to_surface % self.count]

    def add_surface(self, surface: pg.Surface):
        """Adds a new frame to the animation pack.

        Args:
            surface (pg.Surface): The surface to add to the animation.
        """
        self.surfaces.append(surface)
        self.count += 1
        self._animation_seed = randint(0, self.count)

    def set_size(self, size: Size2):
        """Sets the size of the animation pack and rescales existing surfaces.

        Args:
            size (Size2): The new size for the animation pack.
        """
        self.size = size
        self.__rescale_surface__()

    def set_time_to_surface(self, time_to_surface: int):
        """Sets the time interval between frames.

        Args:
            time_to_surface (int): The interval in ticks.
        """
        self.time_to_surface = time_to_surface

    def set_scale(self, scale: float) -> "AnimationPack":
        """Scales the size of the animation pack.

        Args:
            scale (float): The scale factor.

        Returns:
            AnimationPack: The scaled animation pack instance.
        """
        self.size *= scale
        self.__rescale_surface__()
        return self

    def __rescale_surface__(self):
        """Rescales all surfaces in the animation pack to the current size."""
        for surf in range(self.count):
            self.surfaces[surf] = pg.transform.scale(self.surfaces[surf], self.size.tuple)

    def copy(self) -> "AnimationPack":
        """Creates a copy of the animation pack.

        Returns:
            AnimationPack: A new instance with the same data.
        """
        return self.__copy__()

    def __copy__(self) -> "AnimationPack":
        """Performs a shallow copy of the animation pack.

        Returns:
            AnimationPack: A new copy of the animation pack.
        """
        animator_pack = AnimationPack()
        animator_pack.size = self.size
        animator_pack.surfaces = self.surfaces.copy()
        animator_pack.count = self.count
        animator_pack.time_to_surface = self.time_to_surface
        animator_pack._animation_seed = randint(0, self.count)
        return animator_pack
