from libs import SavesManager, CreateSavesDTO
from pathlib import Path

if __name__ == "__main__":
    saves = SavesManager()
    saves.set_path_save(Path.cwd() / "saves")
    saves.load_from_dir()
    saves_names = saves.get_saves_name()
    print(saves_names)
    # print(saves.get_preview_save('test_world'))

    # saves.del_save(saves_names[-1])
    saves.create_saves(CreateSavesDTO(
        name="test_world3",
        version=[0,1,0],
    ))
