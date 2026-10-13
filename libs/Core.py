from pathlib import Path
import json

from libs import Version

paths = ['saves_directory', 'logs_directory', 'mod_packs_directory']


class Core:
    """A singleton class that manages global configurations and paths.

    Attributes:
        version (Version): The version of the application.
        saves_directory (Path): Path to the saves directory.
        logs_directory (Path): Path to the logs directory.
        mod_packs_directory (Path): Path to the mod packs directory.
    """

    version: Version
    saves_directory: Path
    logs_directory: Path
    mod_packs_directory: Path

    def __init__(self):
        """Initializes the Core instance by loading settings from a JSON file.

        The configuration is expected to be at 'src/data/configs/core.json'.
        """
        path = Path.cwd()
        self.path = path.joinpath("src/data/configs/core.json")
        with self.path.open("r") as f:
            core = json.load(f)
        for i in core:
            if i in paths:
                self.__dict__[i] = path.joinpath(core[i])
            elif i == "version":
                self.__dict__[i] = Version(core[i])
            else:
                self.__dict__[i] = core[i]


CORE = Core()
