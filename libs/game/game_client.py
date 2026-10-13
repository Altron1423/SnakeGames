from pathlib import Path

import pygame as pg

from typing import Callable, Generator, Any

from .entitys import ClientPlayer, ClientEnemy
from .. import GameDataToClientDTO, GameDataToServerDTO, loger
from ..ticker import Ticker, MainTicker
from ..loaders.animator_loader import animator_loader, entity_animator_loader
from ..loaders import map_loader
from ..math import Vector2
from ..window.screen import Window
from ..window.camera import Camera

L2 = 2 ** 0.5

class GameClient:
    """Manages the game client-side execution, including rendering, input handling, and communication with the server.

    Attributes:
        camera (Camera): Camera for view management.
        ticker (Ticker): Ticker for timing.
        get_data_from_server (Callable[[], Generator[GameDataToClientDTO, Any, None]]): Function to fetch data from the server.
        send_game_data (Callable[[GameDataToServerDTO], None]): Function to send data to the server.
        window (Window): Window for rendering.
        player (ClientPlayer): Client-side representation of the player.
        entities (dict[str, ClientEnemy]): Client-side representation of entities.
        action (str | None): Current player action.
    """
    camera: Camera
    ticker: Ticker

    get_data_from_server:  Callable[
        [], Generator[GameDataToClientDTO, Any, None]
    ]
    send_game_data: Callable[[GameDataToServerDTO], None]
    window: Window

    player: ClientPlayer
    entities: dict[str, ClientEnemy]

    action: None | str = None

    def __init__(self, player_name: str):
        """Initializes the game client.

        Args:
            player_name (str): The name of the player.
        """
        self.player = ClientPlayer(player_name)
        self.ticker = MainTicker

        path = Path.cwd()
        path_map = path.joinpath("src/data/map")
        path_animator = path.joinpath("src/data/animators")

        animator_loader.load_from_dir(path_animator)
        map_loader.load_from_dir(path_map)

        self.entities = {}

        loger.status("GameMain loaded complete")

    def set_game_data(
            self,
            get_data_from_server: Callable[
                [], Generator[GameDataToClientDTO, Any, None]
            ],
            send_game_data: Callable[[GameDataToServerDTO], None],
            window: Window
    ) -> None:
        """Sets the communication functions and the window.

        Args:
            get_data_from_server (Callable[[], Generator[GameDataToClientDTO, Any, None]]): Function to fetch data.
            send_game_data (Callable[[GameDataToServerDTO], None]): Function to send data.
            window (Window): The window object.
        """
        self.get_data_from_server = get_data_from_server
        self.send_game_data = send_game_data
        self.window = window

        default_player_animator = entity_animator_loader.get("player_animator")
        default_player_animator.set_size(self.player.collision * 4)

        self.camera = Camera(window, self.player, default_player_animator)
        self.camera.entities = self.entities

    def moving_to(self, direction: str):
        """Updates player's orientation based on direction input.

        Args:
            direction (str): The direction string (e.g., 'up_d', 'right_u').
        """
        if direction == "up_d" or direction == "down_u":
            self.player.raw_orientation.z -= 1
        elif direction == "up_u" or direction == "down_d":
            self.player.raw_orientation.z += 1
        elif direction == "right_d" or direction == "left_u":
            self.player.raw_orientation.x += 1
        elif direction == "right_u" or direction == "left_d":
            self.player.raw_orientation.x -= 1

        if self.player.raw_orientation.x != 0 and self.player.raw_orientation.z != 0:
            self.player.orientation = Vector2(
                round(self.player.raw_orientation.x / L2, 3),
                round(self.player.raw_orientation.z / L2, 3)
            )
        else:
            self.player.orientation = self.player.raw_orientation

    def start(self):
        """Starts the game client loop.
        """
        _ = self.send_game_data
        loger.status("GameMain started")

    def draw(self):
        """Renders the current view.
        """
        if self.player.map_block is not None:
            self.camera.set_new_target_position(self.player.position)
            self.camera.update()
            self.window.add_task_draw(1, (self.camera.get_surface(), (0, 0)))

    def update_entities(self, entities):
        """Synchronizes client entities with server data.

        Args:
            entities: The list of entity DTOs received from the server.
        """
        names = list(self.entities.keys())
        for entity in entities:
            if entity.id == self.player.id:
                continue
            ent = self.entities.get(entity.id)
            if ent is None:
                ent = ClientEnemy(entity.id)
                self.entities[entity.id] = ent
                self.camera.was_new = True
            else:
                names.remove(entity.id)
            ent.update_from_server(entity)
        for name in names:
            self.entities.pop(name)

    def main(self):
        """The main game loop iteration.
        """
        if self.ticker % 2:
            dto = self.player.data_to_server()

            dto.action = self.action
            self.action = None

            self.send_game_data(dto)

            for act in self.get_data_from_server():
                self.player.get_data_from_server(act.player)
                self.update_entities(act.entities)
                # self.camera.entities = act.entities
                # if len(act.entities) > 1:
                #     print(act.entities[1:])

        self.draw()

    def action_1(self):
        """Example action handler."""
        self.action = "1"
