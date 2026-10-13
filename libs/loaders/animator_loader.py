from pathlib import Path

from . import Loader
from .entity_animator_loader import EntityAnimatorLoader, entity_animator_loader


class AnimatorLoader(Loader):
    """A loader class for animators.

    This class is responsible for loading animator data from files.
    """
    player_loader: EntityAnimatorLoader = entity_animator_loader
    entity_animator_loader: EntityAnimatorLoader = entity_animator_loader


    @classmethod
    def load_from_dir(cls, path_map: Path) -> None:
        """Loads animators from a directory.

        Args:
            path_map (Path): The directory containing animator files.
        """
        entity_animator_loader.load_from_dir(path_map.joinpath("players"))
        # entity_animator_loader.load_from_dir(path_map.joinpath("entities"))


animator_loader = AnimatorLoader()
