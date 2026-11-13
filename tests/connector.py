# import unittest
from pathlib import Path

from conecting import ClientConnector, ServerConnector
from libs import ConnectClientDTO, CORE, AddressConnectDTO

# class ConnectorTestCase(unittest.TestCase):
#     def test_send_file(self):
#         user_data_client = ConnectClientDTO(
#             version=CORE.version,
#             name="test_client",
#             password="123"
#         )
#         user_data_server = ConnectClientDTO(
#             version=CORE.version,
#             name="test_server",
#             password="123"
#         )
#
#         c_soc = ClientConnector(user_data_client)
#         s_soc = ServerConnector(user_data_server)
#
#         c_soc.start_client()
#         s_soc.start_server()
#
#         a = s_soc.main_socket.getsockname()
#
#         addr = AddressConnectDTO(
#             ip=a[0],
#             port=a[1]
#         )
#
#         c_soc.connect(addr)
#         c_soc.join_game()
#
#         us = s_soc.__find_user__("test_server")


if __name__ == '__main__':
    # unittest.main()
    user_data_client = ConnectClientDTO(
        version=CORE.version,
        name="test_client",
        password="123"
    )
    user_data_server = ConnectClientDTO(
        version=CORE.version,
        name="test_server",
        password="123"
    )

    c_soc = ClientConnector(user_data_client)
    s_soc = ServerConnector(user_data_server)

    c_soc.start_client()
    s_soc.start_server()

    a = s_soc.main_socket.getsockname()

    addr = AddressConnectDTO(
        ip=a[0],
        port=a[1]
    )

    c_soc.connect(addr)
    c_soc.join_game()

    us = s_soc.__find_user__("test_server")




