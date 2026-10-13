from dataclasses import dataclass

from libs.dtos import DimensionSaveDTO, DimensionConfigDTO
from libs.save.dimension import Dimension


@dataclass(frozen=True, slots=True)
class DimensionSaveMapper:
    """Mapper for dimension saving data.

    This class provides static methods to convert between DimensionSaveDTO,
    Dimension objects, and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: DimensionSaveDTO) -> dict:
        """Converts a DimensionSaveDTO to a dictionary.

        Args:
            dto (DimensionSaveDTO): The dimension save data DTO.

        Returns:
            dict: A dictionary representation of the dimension save data.
        """
        return {
            "full_name": dto.full_name,
            "name": dto.name,
            "blocks": dto.blocks,
        }

    @staticmethod
    def dict_to_dto(data: dict) -> DimensionSaveDTO:
        """Converts a dictionary to a DimensionSaveDTO.

        Args:
            data (dict): The dictionary containing dimension save data.

        Returns:
            DimensionSaveDTO: The reconstructed DimensionSaveDTO.
        """
        return DimensionSaveDTO(
            full_name=data["full_name"],
            name=data["name"],
            blocks=data["blocks"]
        )

    @staticmethod
    def dim_to_dto(dim: Dimension) -> DimensionSaveDTO:
        """Converts a Dimension object to a DimensionSaveDTO.

        Args:
            dim (Dimension): The dimension object.

        Returns:
            DimensionSaveDTO: The reconstructed DimensionSaveDTO.
        """
        return DimensionSaveDTO(
            full_name=str(dim),
            name=dim.name,
            blocks=[str(block) for block in dim.blocks]
        )

    @staticmethod
    def update_from_dto(dim: Dimension, dto: DimensionSaveDTO):
        """Updates a Dimension object from a DimensionSaveDTO.

        Args:
            dim (Dimension): The dimension object to update.
            dto (DimensionSaveDTO): The dimension save data DTO.
        """
        dim.full_name = dto.full_name
        dim.name = dto.name

@dataclass(frozen=True, slots=True)
class DimensionConfigMapper:
    """Mapper for dimension configuration data.

    This class provides static methods to convert between DimensionConfigDTO
    and dictionary representations.
    """

    @staticmethod
    def dict_to_dto(data: dict) -> DimensionConfigDTO:
        """Converts a dictionary to a DimensionConfigDTO.

        Args:
            data (dict): The dictionary containing dimension config data.

        Returns:
            DimensionConfigDTO: The reconstructed DimensionConfigDTO.
        """
        return DimensionConfigDTO(
            name=data["name"],
            size=data["size"],
            blocks=data["blocks"]
        )
