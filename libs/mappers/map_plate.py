from dataclasses import dataclass

from libs import MapPlateConfigDTO, MapPlate, MapPlateSaveDTO


@dataclass(frozen=True, slots=True)
class MapPlateSaveMapper:
    """Mapper for map plate saving data.

    This class provides static methods to convert between MapPlateSaveDTO,
    MapPlate objects, and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: MapPlateSaveDTO) -> dict:
        """Converts a MapPlateSaveDTO to a dictionary.

        Args:
            dto (MapPlateSaveDTO): The map plate save data DTO.

        Returns:
            dict: A dictionary representation of the map plate save data.
        """
        return {
            "full_name": dto.full_name,
            "name": dto.name,
            "id": dto.id,
            "type": dto.type,
            "custom_data": dto.custom_data,
        }

    @staticmethod
    def dict_to_dto(data: dict) -> MapPlateSaveDTO:
        """Converts a dictionary to a MapPlateSaveDTO.

        Args:
            data (dict): The dictionary containing map plate save data.

        Returns:
            MapPlateSaveDTO: The reconstructed MapPlateSaveDTO.
        """
        return MapPlateSaveDTO(
            full_name=data["full_name"],
            name=data["name"],
            id=data["id"],
            type=data["type"],
            custom_data=data["custom_data"],
        )

    @staticmethod
    def plate_to_dto(map_chunk: MapPlate) -> MapPlateSaveDTO:
        """Converts a MapPlate object to a MapPlateSaveDTO.

        Args:
            map_chunk (MapPlate): The map plate object.

        Returns:
            MapPlateSaveDTO: The reconstructed MapPlateSaveDTO.
        """
        return MapPlateSaveDTO(
            full_name=str(map_chunk),
            name=map_chunk.name,
            id=map_chunk.id,
            type=map_chunk.type,
            custom_data=map_chunk.get_custom_data()
        )

    @staticmethod
    def update_from_dto(plate: MapPlate, dto: MapPlateSaveDTO):
        """Updates a MapPlate object from a MapPlateSaveDTO.

        Args:
            plate (MapPlate): The map plate object to update.
            dto (MapPlateSaveDTO): The map plate save data DTO.
        """
        plate.full_name = dto.full_name
        plate.name = dto.name
        plate.id = dto.id
        plate.type = dto.type
        plate.custom_data = dto.custom_data

@dataclass(frozen=True, slots=True)
class MapPlateConfigMapper:
    """Mapper for map plate configuration data.

    This class provides static methods to convert between MapPlateConfigDTO
    and dictionary representations.
    """

    @staticmethod
    def dict_to_dto(data: dict) -> MapPlateConfigDTO:
        """Converts a dictionary to a MapPlateConfigDTO.

        Args:
            data (dict): The dictionary containing map plate config data.

        Returns:
            MapPlateConfigDTO: The reconstructed MapPlateConfigDTO.
        """
        return MapPlateConfigDTO(
            name=data["name"],
            type=data["type"],
            color=data["color"],
            texture=data["texture"],
            changeable=data["changeable"],
            layer=data["layer"]
        )
