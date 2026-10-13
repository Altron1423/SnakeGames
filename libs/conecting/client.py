import time
from typing import Any, Generator
from libs import loger
from libs.dtos import (
    AddressConnectDTO, ConnectServerDTO, ConnectClientDTO,
    GameDataToServerDTO, GameDataToClientDTO
)
from libs.mappers import (
    ConnectServerMapper, ConnectClientMapper, GameDataToServerMapper, GameDataToClientMapper
)
from . import SocConnector
from socket import (
    socket, AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
)


class ClientConnector(SocConnector):
    """Client side socket connector.

    Attributes:
        connect_data (ConnectClientDTO | None): Connection data from client.
        data_from_server (GameDataToClientDTO | None): Data received from server.
    """
    connect_data: ConnectClientDTO | None = None
    data_from_server: GameDataToClientDTO | None = None

    def __init__(self, dto: ConnectClientDTO):
        """Initializes the ClientConnector.

        Args:
            dto (ConnectClientDTO): Client connection data.
        """
        super().__init__(dto.version)
        self.connect_data = dto

    def start_client(self):
        """Starts the client socket.
        """
        self.main_socket = socket(AF_INET, SOCK_STREAM)
        self.main_socket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)

    def set_data(self, dto: ConnectClientDTO):
        """Sets the client connection data.

        Args:
            dto (ConnectClientDTO): The connection data.
        """
        self.game_version = dto.version
        self.connect_data = dto

    def main(self, tick: int = None):
        """Main loop for the client.

        Args:
            tick (int, optional): Current tick. Defaults to None.
        """
        try:
            raw_server_message: str | dict | None = self.decode_message(
                self.__receive__(), True
            )
            # loger.log(f"Server message: {raw_server_message}")
            if raw_server_message is not None:
                if type(raw_server_message) is str:
                    if raw_server_message == self.server_close:
                        self.close()
                else:
                    server_answer = raw_server_message.get(self.game_status_message)
                    if server_answer is not None:
                        dto = GameDataToClientMapper.dict_to_dto(server_answer)
                        self.data_from_server = dto

        except BlockingIOError:
            pass

    def connect(self, address: AddressConnectDTO) -> None:
        """Connects to the specified address.

        Args:
            address (AddressConnectDTO): The address to connect to.
        """
        loger.log(f"Connect to {(address.ip, self.server_port)}")
        self.main_socket.connect((address.ip, self.server_port))

    def disconnect(self):
        """Disconnects from the server."""
        self.__send__(self.drop_connect)

    def close(self):
        """Closes the connection.
        """
        try:
            self.disconnect()
        except OSError:
            pass
        super().close()

    def get_data_from_server(self) -> Generator[GameDataToClientDTO, Any, None]:
        """Generator for data received from the server.

        Yields:
            GameDataToClientDTO: The next piece of data from the server.
        """
        if self.data_from_server is not None:
            d = self.data_from_server
            self.connect_data = None
            yield d

    def send_game_data(self, dto: GameDataToServerDTO):
        """Sends game data to the server.

        Args:
            dto (GameDataToServerDTO): The game data to send.
        """
        self.__send__({
            self.game_status_message: GameDataToServerMapper.dto_to_dict(dto)
        })

    def join_game(self) -> bool:
        """Attempts to join the game.

        Returns:
            bool: True if successfully joined, False otherwise.
        """
        if self.connect_data is not None:
            self.__send__({
                self.join_in_game_message: ConnectClientMapper.dto_to_dict(self.connect_data)
            })
            connection = self.__receive__()
            if self.decode_message(connection, True) == self.true_join_game:
                self.main_socket.setblocking(False)
                return True
        return False

    def find_servers(self) -> list[ConnectServerDTO]:
        """Finds available servers.

        Returns:
            list[ConnectServerDTO]: A list of discovered servers.
        """
        address_list = self.ad_checker.start()
        print(address_list)
        servers_list: list[ConnectServerDTO] = []
        if len(address_list) > 0:
            self.start_client()
            for address in address_list:
                if connect_data := self.__testing_is_server__(address):
                    servers_list.append(connect_data)
                time.sleep(0.5)
            self.close()
        return servers_list

    def __testing_is_server__(self, address: AddressConnectDTO) -> ConnectServerDTO | None:
        """Tests if a given address is a server.

        Args:
            address (AddressConnectDTO): The address to test.

        Returns:
            ConnectServerDTO | None: The server info if found, otherwise None.
        """
        answer = None
        try:
            # self.main_socket.settimeout(0.4)
            self.connect(address)
            self.__send__(self.testing_server_message)

            raw_server_answer: str | dict | None = self.decode_message(
                self.__receive__()
            )
            server_answer = raw_server_answer.get(self.true_server_testing)
            if server_answer is not None:
                dto = ConnectServerMapper.dict_to_dto(server_answer)
                dto.address = address
                if dto.version != self.game_version:
                    pass
                else:
                    answer = dto
            self.disconnect()
        except ConnectionRefusedError:
            loger.error("ConnectionRefusedError")
        except PermissionError:
            loger.error("PermissionError")
        except OSError:
            loger.error("OSError")

        return answer
