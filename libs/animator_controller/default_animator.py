import pygame as pg
from .animation_pack import AnimationPack
from libs.math import Size2
from libs.ticker import Tick


class DefaultAnimator:
    """An animator that manages and scales animation packs.

    Attributes:
        default_surface (dict[str, AnimationPack]): Maps animation names to their original packs.
        default_size (Size2): The default size for animations.
        first_scale (float): The first scale factor.
        second_scale (float): The second scale factor.
        scale_surface (dict[str, AnimationPack]): Maps animation names to their scaled packs.
        type (str | None): The currently active animation type.
        tick (Tick): The current tick reference.
    """

    default_surface: dict[str, AnimationPack]
    default_size: Size2
    first_scale: float
    second_scale: float
    scale_surface: dict[str, AnimationPack]
    type: str | None
    tick: Tick

    def __init__(self, tick: Tick):
        """Initializes the DefaultAnimator.

        Args:
            tick (Tick): The tick to use for animations.
        """
        self.default_surface = {}
        self.first_scale = 1.0
        self.second_scale = 1.0
        self.scale_surface = {}
        self.type = None
        self.tick = tick

    def get_surface(self) -> None | pg.Surface:
        """Gets the current surface for the active animation type.

        Returns:
            None | pg.Surface: The current surface, or None if no type is set.
        """
        if self.type is None:
            return None
        return self.scale_surface[self.type].get_surface(int(self.tick))

    def add_animation_pack(self, name: str, animator_pack: AnimationPack):
        """Adds an animation pack to the animator.

        Args:
            name (str): The name of the animation.
            animator_pack (AnimationPack): The animation pack to add.
        """
        self.default_surface[name] = animator_pack
        animator_pack = animator_pack.copy()
        animator_pack.set_scale(self.first_scale * self.second_scale)
        self.scale_surface[name] = animator_pack

    def set_type(self, type_d: str):
        """Sets the active animation type.

        Args:
            type_d (str): The name of the animation type to set.
        """
        if type_d in self.default_surface:
            self.type = type_d

    def set_scale(self, scale: float):
        """Sets the scale for the animations.

        Args:
            scale (float): The scale factor.
        """
        if self.second_scale != scale:
            self.second_scale = scale
            self.__rescale__()

    def set_default_size(self, size: Size2):
        """Sets the default size for animations.

        Args:
            size (Size2): The default size.
        """
        self.default_size = size

    def set_size(self, size: Size2):
        """Sets the size and calculates the scale factor.

        Args:
            size (Size2): The target size.
        """
        self.first_scale = (size / self.default_size).x

    def __rescale__(self):
        """Rescales all animation packs in the scale_surface."""
        for name in self.default_surface:
            self.scale_surface[name] = self.default_surface[name].copy().set_scale(self.first_scale * self.second_scale)

    def __copy__(self) -> "DefaultAnimator":
        """Performs a deep copy of the animator.

        Returns:
            DefaultAnimator: A new copy of the animator.
        """
        anim = self.__class__(self.tick)
        anim.set_default_size(self.default_size)
        anim.first_scale = self.first_scale
        anim.set_scale(self.second_scale)
        anim.set_type(self.type)
        for i in self.default_surface:
            anim.add_animation_pack(i, self.default_surface[i])
        return anim
