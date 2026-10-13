import json
from pathlib import Path

from ..game import Player
from libs.loaders.loader import Loader
from libs.mappers.player import PlayerLoadMapper


class PlayerLoader(Loader):
    """A loader class for players.

    This class is responsible for loading player data from files.
    """
    elements: dict[str, Player]

    def load(self, path: Path) -> None:
        """Loads a player from a specified path.

        Args:
            path (Path): The path to the file containing player data.
        """
        with Path(path).open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] in ["entity", "player"]:
                dto = PlayerLoadMapper.dict_to_dto(json_data["data"])
                player = Player.load_from_config(dto)

                self.add(player, dto.race)

    def get(self, name: str) -> Player | None:
        """Retrieves a player by name.

        Args:
            name (str): The name of the player.

        Returns:
            Player | None: The player object if found, otherwise None.
        """
        return super().get(name)

    def get_new(self, name: str) -> Player | None:
        """Retrieves a player or returns a new one if not found.

        Args:
            name (str): The name of the player.

        Returns:
            Player | None: The player object.
        """
        return super().get_new(name)


player_loader = PlayerLoader()
