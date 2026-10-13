import json
import scapy.all as sc
from libs import Version, loger
from libs.dtos import AddressConnectDTO
from socket import (
    socket, gethostbyname, gethostname
)


class AddressChecker:
    """Handles network address checking.

    Attributes:
        local_ip (str): Local IP address.
        ip_mac_network (dict): Map of IP to MAC addresses.
    """
    def __init__(self, ip: str):
        """Initializes the AddressChecker.

        Args:
            ip (str): The local IP address to scan.
        """
        self.local_ip = ip
        self.ip_mac_network = {}

    def start(self, output_info: bool = False) -> list:
        """Starts the scanning of the network.

        Args:
            output_info (bool): Whether to print the found devices.

        Returns:
            list: A list of found AddressConnectDTOs.
        """
        ip_list = self.local_ip.split(".")
        self.ip_mac_network = self.get_ip_mac_network(
            f'{ip_list[0]}.{ip_list[1]}.{ip_list[2]}.1/24', output_info
        )

        if output_info:
            self.print_ip_mac(self.ip_mac_network)
        return self.ip_mac_network

    @staticmethod
    def get_ip_mac_network(ip: str, verbose: bool = False) -> list[AddressConnectDTO]:
        """Scans the network for active IP/MAC pairs.

        Args:
            ip (str): The IP range to scan.
            verbose (bool): Whether to use verbose mode in scapy.

        Returns:
            list[AddressConnectDTO]: A list of found devices.
        """
        answered_list = sc.srp(sc.Ether(dst='ff:ff:ff:ff:ff:ff') / sc.ARP(pdst=ip), timeout=1, verbose=verbose)[0]
        clients_list = []
        for element in answered_list:
            clients_list.append(
                AddressConnectDTO(
                    ip=element[1].psrc,
                    mac=element[1].hwsrc,
                )
            )
        return clients_list

    @staticmethod
    def print_ip_mac(mac_ip_list):
        """Prints the IP/MAC list to the console.

        Args:
            mac_ip_list (list): List of address info.
        """
        print(f"\nMachine in Network:\n\nIP\t\t\t\t\tMAC-address\n{'-' * 41}")
        for client in mac_ip_list:
            print(f'{client["ip"]}\t\t{client["mac"]}')


class SocConnector:
    """Base class for socket communication.

    Attributes:
        ad_checker (AddressChecker): Checker for local network.
        game_version (Version): Version of the game.
        LOCALHOST (str): The local IP address.
        main_socket (socket | None): The main socket used for connection.
        server_port (int): The port for the server.
        testing_server_message (str): Message to test server presence.
        true_server_testing (str): Successful server test response.
        drop_connect (str): Message for dropping connection.
        join_in_game_message (str): Message for joining game.
        true_join_game (str): Successful join response.
        false_join_game (str): Failed join response.
        game_status_message (str): Message key for game status.
        server_close (str): Message for closing the server.
    """
    ad_checker: AddressChecker
    game_version: Version
    LOCALHOST: str
    main_socket: socket | None = None
    server_port: int = 10000
    testing_server_message: str = "WAY_IC"
    true_server_testing: str = "YIS"
    drop_connect: str = "COM_DROP"
    join_in_game_message: str = "COM_JOIN"
    true_join_game: str = "JOIN_TRUE"
    false_join_game: str = "JOIN_FALSE"
    game_status_message: str = "GAME_STATUS"
    server_close: str = "CLOSE"

    def __init__(self, version: Version):
        """Initializes the SocConnector.

        Args:
            version (Version): The version of the game.
        """
        self.game_version = version
        self.LOCALHOST = self.local_ipv4()
        self.ad_checker = AddressChecker(self.LOCALHOST)

    @staticmethod
    def local_ipv4():
        """Gets the local IPv4 address.

        Returns:
            str: The local IPv4 address.
        """
        ip_l = gethostbyname(gethostname())
        return ip_l

    def close(self):
        """Closes the main socket."""
        if self.main_socket is not None:
            self.main_socket.close()
            self.main_socket = None

    @staticmethod
    def decode_message(raw_message: bytes | str, string:bool=False):
        """Decodes a message.

        Args:
            raw_message (bytes | str): The raw message.
            string (bool): Whether to return as string.

        Returns:
            str | dict | None: Decoded message or None if failed.
        """
        if type(raw_message) == bytes:
            raw_message = raw_message.decode()
        # loger.log(f"{raw_message=}")
        # last = raw_message.find(">")
        last = -1
        if len(raw_message) and raw_message[0] == '<' and raw_message[last] == '>':
            message = raw_message[1:last]
            try:
                return json.loads(message)
            except json.decoder.JSONDecodeError as e:
                if string:
                    return message
            return None
        else:
            return None

    def __send__(self, message: str | dict) -> None:
        """Sends a message via the socket.

        Args:
            message (str | dict): Message to send.
        """
        if self.main_socket is None:
            return
        if type(message) == dict:
            message = json.dumps(message)
        self.main_socket.send(f"<{message}>".encode())

    def __receive__(self) -> bytes:
        """Receives data from the socket.

        Returns:
            bytes: Received raw bytes.
        """
        return self.main_socket.recv(1024)
