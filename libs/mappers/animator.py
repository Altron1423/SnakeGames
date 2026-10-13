from dataclasses import dataclass

from ..math import Size2
from libs.dtos import (
    AnimationPackDataDTO, AnimatorDataDTO,
)


@dataclass(frozen=True, slots=True)
class AnimationPackDataMapper:
    """Mapper for animation pack data.

    This class provides static methods to convert between AnimationPackDataDTO
    and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: AnimationPackDataDTO) -> dict[str, str | int]:
        """Converts an AnimationPackDataDTO to a dictionary.

        Args:
            dto (AnimationPackDataDTO): The animation pack data DTO.

        Returns:
            dict[str, str]: A dictionary representation of the animation pack data.
        """
        return {
            "texture": dto.texture,
            "length": dto.length,
            "speed": dto.speed,
            "line": dto.line
        }

    @staticmethod
    def dict_to_dto(data: dict) -> AnimationPackDataDTO:
        """Converts a dictionary to an AnimationPackDataDTO.

        Args:
            data (dict): The dictionary containing animation pack data.

        Returns:
            AnimationPackDataDTO: The reconstructed AnimationPackDataDTO.
        """
        return AnimationPackDataDTO(
            texture=data["texture"],
            length=data["length"],
            speed=data["speed"],
            line=data["line"]
        )

@dataclass(frozen=True, slots=True)
class AnimatorDataMapper:
    """Mapper for animator data.

    This class provides static methods to convert between AnimatorDataDTO
    and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: AnimatorDataDTO) -> dict[str, str | dict]:
        """Converts an AnimatorDataDTO to a dictionary.

        Args:
            dto (AnimatorDataDTO): The animator data DTO.

        Returns:
            dict[str, str]: A dictionary representation of the animator data.
        """
        animation_pack = {}
        animation_pack_data = dto.animation_pack
        for name_pack in animation_pack_data:
            animation_pack[name_pack] = AnimationPackDataMapper.dto_to_dict(animation_pack_data[name_pack])
        return {
            "name": dto.name,
            "size": str(dto.size),
            "animation_pack": animation_pack
        }

    @staticmethod
    def dict_to_dto(data: dict) -> AnimatorDataDTO:
        """Converts a dictionary to an AnimatorDataDTO.

        Args:
            data (dict): The dictionary containing animator data.

        Returns:
            AnimatorDataDTO: The reconstructed AnimatorDataDTO.
        """
        animation_pack = {}
        animation_pack_data = data["animation_pack"]
        for name_pack in animation_pack_data:
            animation_pack[name_pack] = AnimationPackDataMapper.dict_to_dto(animation_pack_data[name_pack])
        return AnimatorDataDTO(
            name=data["name"],
            size=Size2(data["size"]),
            animation_pack=animation_pack
        )
