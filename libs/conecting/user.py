from socket import socket
from hashlib import sha1
from typing import Any, Generator

from libs import GameDataToServerDTO, GameDataToClientDTO


def hash(password: str) -> str:
    """Hashes a password using SHA-1.

    Args:
        password (str): The password to hash.

    Returns:
        str: The SHA-1 hash of the password.
    """
    return sha1(password.encode()).hexdigest()


class User:
    """Represents a user in the game.

    Attributes:
        name (str): Name of the user.
        password (str): Hashed password of the user.
        connect (socket | str | None): Connection associated with the user.
        user_action (list[GameDataToServerDTO]): List of actions from the user.
        server_data (GameDataToClientDTO | None): Last received data from the server.
    """
    name: str
    password: str
    connect: socket | str | None
    user_action: list[GameDataToServerDTO]
    server_data: GameDataToClientDTO | None

    def __init__(self, name: str, password: str):
        """Initializes a User instance.

        Args:
            name (str): Name of the user.
            password (str): Password of the user.
        """
        self.name = name
        self.password = hash(password)
        self.connect = None
        self.user_action = []
        self.server_data = None

    def test_password(self, password: str) -> bool:
        """Checks if the provided password is correct.

        Args:
            password (str): The password to test.

        Returns:
            bool: True if correct, False otherwise.
        """
        return hash(password) == self.password

    def add_message(self, dto: GameDataToServerDTO):
        """Adds a message to the user's action list.

        Args:
            dto (GameDataToServerDTO): The message to add.
        """
        self.user_action.append(dto)

    def send_to_user(self, dto: GameDataToClientDTO):
        """Sets the user's data from the server.

        Args:
            dto (GameDataToClientDTO): The data to send to the user.
        """
        self.server_data = dto

    @property
    def get_user_action(self) -> Generator[GameDataToServerDTO, Any, None]:
        """Generator to iterate over user actions.

        Yields:
            GameDataToServerDTO: The next user action.
        """
        for i in self.user_action:
            yield i
        self.user_action = []

    @property
    def get_data_from_server(self) -> Generator[GameDataToClientDTO, Any, None]:
        """Generator to iterate over server data.

        Yields:
            GameDataToClientDTO: The next piece of server data.
        """
        if self.server_data:
            yield self.server_data
        self.server_data = None
