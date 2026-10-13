from dataclasses import dataclass

from libs import DataSaveDTO


@dataclass(frozen=True, slots=True)
class SaveMapper:
    """Mapper for game save data.

    This class provides static methods to convert between DataSaveDTO,
    Save objects, and dictionary representations.
    """

    @staticmethod
    def dto_to_dict(dto: DataSaveDTO) -> dict:
        """Converts a DataSaveDTO to a dictionary.

        Args:
            dto (DataSaveDTO): The save data DTO.

        Returns:
            dict: A dictionary representation of the save data.
        """
        return {
            "name": dto.name,
            "version": ".".join(map(str, dto.version)),
            "description": dto.description,
            "last_open": dto.last_open,
            "created": dto.created,
        }

    @staticmethod
    def dict_to_dto(data: dict) -> DataSaveDTO:
        """Converts a dictionary to a DataSaveDTO.

        Args:
            data (dict): The dictionary containing save data.

        Returns:
            DataSaveDTO: The reconstructed DataSaveDTO.
        """
        return DataSaveDTO(
            name=data["name"],
            version=list(map(int, data["version"].split("."))),
            description=data["description"],
            last_open=data["last_open"],
            created=data["created"],
        )

    @staticmethod
    def save_to_dto(save) -> DataSaveDTO:
        """Converts a Save object to a DataSaveDTO.

        Args:
            save: The save object.

        Returns:
            DataSaveDTO: The reconstructed DataSaveDTO.
        """
        changes_plates = {}
        for position in save.size:
            plate = save.get_plate(position)
            if plate.changeable:
                changes_plates[str(position)] = str(plate)
        return DataSaveDTO(
            name=save.name,
            version=save.version,
            description=save.description,
            last_open=save.last_open,
            created=save.created,
        )

    @staticmethod
    def update_from_dto(save, dto: DataSaveDTO) -> None:
        """Updates a Save object from a DataSaveDTO.

        Args:
            save: The save object to update.
            dto (DataSaveDTO): The save data DTO.
        """
        save.name = dto.name
        save.version = dto.version
        save.description = dto.description
        save.last_open = dto.last_open
        save.created = dto.created
