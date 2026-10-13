from dataclasses import dataclass

from ..math import Size2


@dataclass
class AnimationPackDataDTO:
    """Data Transfer Object for an animation pack's frame data.

    Attributes:
        texture (str): Path or identifier of the texture.
        length (int): Number of frames in the animation.
        speed (int): Animation speed.
        line (int): The line/row in the texture where the animation is located.
    """
    texture: str
    length: int
    speed: int
    line: int


@dataclass
class AnimatorDataDTO:
    """Data Transfer Object for animator state.

    Attributes:
        name (str): Name of the animation.
        size (Size2): Size of the animation frames.
        animation_pack (dict[str, AnimationPackDataDTO]): Dictionary mapping animation names to their data.
    """
    name: str
    size: Size2
    animation_pack: dict[str, AnimationPackDataDTO]
