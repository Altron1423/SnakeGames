from pathlib import Path
from datetime import datetime

from libs.dtos.save import (
    CreateSavesDTO,
    PresentationSaveDTO,
    CreateSaveWF_DTO
)
from libs.Loger import loger
from libs.save.save_full import SaveFull
from libs.save.save_light import SaveLight

class SavesManager:
    """Manages the creation, loading, and deletion of saves.

    Attributes:
        path_saves (Path): The directory where saves are stored.
        load_save (SaveFull | None): The currently loaded full save.
        saves (list[SaveLight]): A list of all available light saves.
        full_load_save (SaveFull | None): The currently loaded full save.
        using_dir (list[Path]): A list of directories being used.
    """
    path_saves: Path
    load_save: SaveFull | None
    saves: list[SaveLight] = []
    full_load_save: SaveFull | None
    using_dir: list[Path] = []

    @classmethod
    def set_path_save(cls, path_saves: Path) -> None:
        """Sets the path where saves are stored.

        Args:
            path_saves (Path): The path to the saves directory.
        """
        cls.path_saves = path_saves

    @classmethod
    def load_from_dir(cls) -> None:
        """Loads all light saves from the configured directory.
        """
        if cls.path_saves in cls.using_dir:
            return
        cls.using_dir.append(cls.path_saves)
        for iPath in cls.path_saves.iterdir():
            cls.__load_light_save(iPath)

    @classmethod
    def get_saves_name(cls) -> list[str]:
        """Gets the names of all available saves.

        Returns:
            list[str]: A list of save names.
        """
        save_names = []
        for save in cls.saves:
            save_names.append(save.name)
        return save_names

    @classmethod
    def get_preview_save(cls, name_save: str) -> PresentationSaveDTO | None:
        """Gets a preview of a specific save.

        Args:
            name_save (str): The name of the save to get a preview for.

        Returns:
            PresentationSaveDTO | None: The preview DTO, or None if the save is not found.
        """
        save_element = cls.__get_saves(name_save)

        if not save_element:
            return None

        return PresentationSaveDTO(
            name=save_element.name,
            version=save_element.version,
            last_open=save_element.last_open,
            description=save_element.description,
        )

    @classmethod
    def create_saves(cls, save: CreateSavesDTO) -> bool:
        """Creates a new save.

        Args:
            save (CreateSavesDTO): The DTO containing new save information.

        Returns:
            bool: True if the save was created successfully, False otherwise.
        """
        from libs.file_works import SavesWF

        if save.name in cls.get_saves_name():
            return False

        SavesWF.create_save(CreateSaveWF_DTO(
            name=save.name,
            version=save.version,
            last_open=datetime.now(),
            description="This is test world.",
            path_to_save=cls.path_saves
        ))

        return True

    @classmethod
    def load_full_save(cls, save_name: str) -> SaveFull:
        """Loads a full save by name.

        Args:
            save_name (str): The name of the full save to load.

        Returns:
            SaveFull: The loaded full save.
        """
        return cls.__load_full_save(save_name)

    @classmethod
    def del_save(cls, save_name: str):
        """Deletes a save by name.

        Args:
            save_name (str): The name of the save to delete.
        """
        save = cls.__get_saves(save_name)
        save.delete()
        cls.saves.remove(save)

    @classmethod
    def __get_saves(cls, name: str) -> SaveLight | None:
        """Internal method to get a light save by name.

        Args:
            name (str): The name of the save.

        Returns:
            SaveLight | None: The save object, or None if not found.
        """
        for i_save in cls.saves:
            if i_save.name == name:
                return i_save
        return None

    @classmethod
    def __load_light_save(cls, path: Path) -> None:
        """Internal method to load a light save from a path.

        Args:
            path (Path): The path to the save file.
        """
        try:
            from libs.Loger import loger
            loger.status("load save from:", path)
            save = SaveLight(path)
            save.fast_load()
            cls.saves.append(save)
        except Exception as e:
            from libs.Loger import loger
            loger.status("load save failed")
            loger.error(e)

    @classmethod
    def __load_full_save(cls, save_name: str) -> SaveFull | None:
        """Internal method to load a full save by name.

        Args:
            save_name (str): The name of the full save.

        Returns:
            SaveFull | None: The loaded full save, or None if not found.
        """
        save = cls.__get_saves(save_name)
        if not save:
            return None
        full_save = SaveFull(save)
        return full_save

if __name__ == "__main__":
    saves = SavesManager()
    saves.set_path_save(Path.cwd().joinpath("/saves"))
    saves.load_from_dir()
    saves_names = saves.get_saves_name()
    print(saves_names)
    # print(saves.get_preview_save('test_world'))

    # saves.del_save(saves_names[-1])
    saves.create_saves(CreateSavesDTO(
        name="test_world3",
        version=[0,1,0],
    ))
