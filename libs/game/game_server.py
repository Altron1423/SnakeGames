from pathlib import Path
from typing import Callable, Generator, Any

from . import GameStartException
from libs.save import SaveFull
from libs.generators import SaveCreateTest
from .entitys import Player, Enemy
from .. import GameDataToClientDTO, GameDataToServerDTO
from ..Loger import loger
from ..loaders.entity_loader import player_loader


class GameServer:
    """Manages the game server-side execution, including player connections, entity updates, and saving game state.

    Attributes:
        save (SaveFull): Instance for managing game state persistence.
        get_user_action (Callable[[], Generator[tuple[GameDataToServerDTO, str], Any, None]]): Function to get player actions.
        send_to_user (Callable[[GameDataToClientDTO, str], None]): Function to send data to users.
        load_players (dict[str, Player]): Dictionary of all loaded player objects.
        players_in_game (dict[str, Player]): Dictionary of players currently in the game.
    """
    save: SaveFull
    get_user_action:  Callable[
        [], Generator[
            tuple[GameDataToServerDTO, str],
            Any, None
        ]
    ]
    send_to_user: Callable[[GameDataToClientDTO, str], None]
    load_players: dict[str, Player]
    players_in_game: dict[str, Player]

    def __init__(self):
        """Initializes the game server."""
        path = Path.cwd()
        path_player = path.joinpath("src/data/entities")

        player_loader.load_from_dir(path_player)

        loger.status("GameMain loaded complete")

        self.load_players = {}
        self.players_in_game = {}

    def set_game_data(
            self, save_full: SaveFull,
            get_user_action: Callable[
                [], Generator[
                    tuple[GameDataToServerDTO, str],
                    Any, None
                ]
            ],
            send_to_user: Callable[[GameDataToClientDTO, str], None],
            player_name: str
    ) -> None:
        """Sets the game data and initializes the player.

        Args:
            save_full (SaveFull): The saving instance.
            get_user_action (Callable): Function to get player actions.
            send_to_user (Callable): Function to send data.
            player_name (str): The name of the player.
        """
        self.save = save_full
        if self.save.need_created():
            SaveCreateTest.create(self.save)
        self.get_user_action = get_user_action
        self.send_to_user = send_to_user
        player =  self.summon_new_player(player_name)
        self.players_in_game[player_name] = player

    def summon_new_player(self, name: str) -> Player:
        """Creates and initializes a new player.

        Args:
            name (str): The player's name.

        Returns:
            Player: The newly created player instance.
        """
        player = player_loader.get_new("human")
        player.transition_to(self.save.spawn_map_block)
        player.set_default(name, self.save.spawn_position)
        self.load_players[name] = player
        return player

    def player_connect(self, name: str) -> Player:
        """Handles a player connection.

        Args:
            name (str): The player's name.

        Returns:
            Player: The connected player instance.
        """
        player = self.load_players.get(name)
        if player is None:
            player = self.summon_new_player(name)
        else:
            player.connect()
        self.players_in_game[name] = player
        return player

    def player_disconnect(self, name: str):
        """Handles a player disconnection.

        Args:
            name (str): The player's name.
        """
        player = self.load_players.get(name)
        player.disconnect()
        self.players_in_game.pop(name)

    def start(self):
        """Starts the server.

        Raises:
            GameStartException: If the save object is not set.
        """
        if not self.save:
            raise GameStartException()
        loger.status("GameMain started")

    def main(self):
        """The main server loop iteration."""
        for act, user_name in self.get_user_action():
            player = self.players_in_game[user_name]
            # loger.log(f"Server {user_name=} act.move={act.move}")

            player.set_changes_from_client(act)
            player.update()
            # if player.name != "test_client":
            #     print(player.get_near_entity(100))
            if act.action == "1":
                self.summon_enemyTESTING(player)

            self.send_to_user(
                player.get_data_for_client(),
                user_name
            )
        self.save.update()

    def saving(self):
        """Saves the current game state."""
        self.save.saving()
        loger.status("GameMain saving")

    def summon_enemyTESTING(self, player: Player) -> None:
        """Spawns a test enemy near a player.

        Args:
            player (Player): The player near which to spawn the enemy.
        """
        enemy = Enemy()
        enemy.position = player.position + 0
        player.map_block.add_enemy(enemy)
