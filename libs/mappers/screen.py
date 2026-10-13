from dataclasses import dataclass

from libs.dtos import (
    ButtonDTO, WindowDataDTO,
    WindowDTO
)
from libs.math import Recalc, Vector2


@dataclass(frozen=True, slots=True)
class ButtonMapper:
    """Mapper for button data.

    This class provides static methods to convert between ButtonDTO
    and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: ButtonDTO) -> dict[str, str]:
        """Converts a ButtonDTO to a dictionary.

        Args:
            dto (ButtonDTO): The button data DTO.

        Returns:
            dict[str, str]: A dictionary representation of the button data.
        """
        return {
            "type": dto.type,
            "position": str(dto.position),
            "size": str(dto.size),
            "polygons_name": dto.polygons_name,
            "text": dto.text,
            "png_name": dto.png_name
        }

    @staticmethod
    def dict_to_dto(data: dict) -> ButtonDTO:
        """Converts a dictionary to a ButtonDTO.

        Args:
            data (dict): The dictionary containing button data.

        Returns:
            ButtonDTO: The reconstructed ButtonDTO.
        """
        triggers: dict[tuple[str, bool], str] = {}
        for i, command in data.get("triggers", {}).items():
            dt = i.split("/")
            if len(dt) == 1:
                triggers[(dt[0], False)] = command
                triggers[(dt[0], True)] = command
            elif len(dt) == 2:
                triggers[(dt[0], dt[1] == 'd')] = command
        position = data.get("position")
        if position is not None:
            position = Recalc.load_from_str(position)
        size = data.get("size")
        if size is not None:
            size = Recalc.load_from_str(size)
        return ButtonDTO(
            type=data["type"],
            position=position,
            size=size,
            polygons_name=data["polygons_name"],
            text=data.get("text"),
            triggers=triggers,
            png_name=data.get("png_name")
        )

@dataclass(frozen=True, slots=True)
class WindowDataMapper:
    """Mapper for window data.

    This class provides static methods to convert between WindowDataDTO
    and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: WindowDataDTO) -> dict[str, str | list]:
        """Converts a WindowDataDTO to a dictionary.

        Args:
            dto (WindowDataDTO): The window data DTO.

        Returns:
            dict[str, str | list]: A dictionary representation of the window data.
        """
        return {
            "recalc_position": str(dto.recalc_position),
            "recalc_size": str(dto.recalc_size),
            "default_polygonizer": dto.default_polygonizer,
            "window_background": dto.background,
            "cord_new_button": dto.cord_new_button,
        }

    @staticmethod
    def dict_to_dto(data: dict[str, list | str]) -> WindowDataDTO:
        """Converts a dictionary to a WindowDataDTO.

        Args:
            data (dict[str, list | str]): The dictionary containing window data.

        Returns:
            WindowDataDTO: The reconstructed WindowDataDTO.
        """
        if "window_position" in data:
            recalc_position = Recalc.load_from_str(data["window_position"])
        else:
            recalc_position = Recalc()
        if "window_size" in data:
            recalc_size = Recalc.load_from_str(data["window_size"])
        else:
            recalc_size = Recalc(Vector2(1,1))
        return WindowDataDTO(
            recalc_position=recalc_position,
            recalc_size=recalc_size,
            default_polygonizer=data.get("default_polygonizer"),
            background=data.get("window_background", [30, 30, 30]),
            cord_new_button=data.get("cord_new_button", [0.03, 0.01, 0.04, 0.02, 0.45, 0.3])
        )

@dataclass(frozen=True, slots=True)
class WindowMapper:
    """Mapper for window data.

    This class provides static methods to convert between WindowDTO
    and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: WindowDTO) -> dict[str, str | dict | list[dict]]:
        """Converts a WindowDTO to a dictionary.

        Args:
            dto (WindowDTO): The window DTO.

        Returns:
            dict[str, str]: A dictionary representation of the window data.
        """
        return {
            "name": dto.name,
            "data": WindowDataMapper.dto_to_dict(dto.data),
            "buttons": [ButtonMapper.dto_to_dict(button) for button in dto.buttons]
        }

    @staticmethod
    def dict_to_dto(data: dict[str, str | dict | list]) -> WindowDTO:
        """Converts a dictionary to a WindowDTO.

        Args:
            data (dict[str, str | dict | list]): The dictionary containing window data.

        Returns:
            WindowDTO: The reconstructed WindowDTO.
        """
        return WindowDTO(
            name=data["name"],
            data=WindowDataMapper.dict_to_dto(data["data"]),
            buttons=[ButtonMapper.dict_to_dto(button) for button in data["buttons"]]
        )
