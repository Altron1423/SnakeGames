from libs import GameDataToServerDTO, map_block_loader
from libs.dtos.player import ClientPlayerDTO
from libs.math import Position2, Vector2
from .player import Player


class ClientPlayer(Player):
    """Represents a player on the client side.

    Inherits from the Player class and provides client-side logic such as
    handling server updates and preparing data for transmission.
    """
    raw_orientation: Vector2
    map_block_name: str
    target_position: Position2
    last_direction_view: str

    def __init__(self, player_name: str):
        """Initializes a new ClientPlayer instance.

        Args:
            player_name (str): The player's name.
        """
        super().__init__()
        self.raw_orientation = Vector2(0, 0)
        self.player_name = player_name
        self.target_position = Position2()
        self.last_direction_view = 'down'

    def preferential_orientation(self) -> str:
        """Returns the combined action and direction string.

        Returns:
            str: A string like 'run_right' or 'idle_down'.
        """
        return f"{self.type_action}_{self.direction_view}"

    def get_data_from_server(self, dto: ClientPlayerDTO):
        """Updates client-side player data from server DTO.

        Args:
            dto (ClientPlayerDTO): The DTO containing server-side player data.
        """
        self.name = dto.name
        self.id = dto.id
        self.position = dto.position
        self.health = dto.health
        self.mana = dto.mana
        self.xp = dto.xp
        self.lvl = dto.lvl
        self.map_block = map_block_loader.get(dto.map_block)

    def data_to_server(self) -> GameDataToServerDTO:
        """Prepares player data for transmission to the server.

        Returns:
            GameDataToServerDTO: The DTO containing player data.
        """
        return GameDataToServerDTO(
            move=self.orientation,
            speed=1.0,
            target_position=self.target_position,
            action=None
        )

    @property
    def direction_view(self) -> str:
        """Updates and returns the current direction view string.

        Returns:
            str: The current direction ('right', 'left', 'down', or 'up').
        """
        if self.orientation.x > 0:
            self.last_direction_view = 'right'
        elif self.orientation.x < 0:
            self.last_direction_view = 'left'
        elif self.orientation.z > 0:
            self.last_direction_view = 'down'
        elif self.orientation.z < 0:
            self.last_direction_view = 'up'
        return self.last_direction_view

    @property
    def type_action(self) -> str:
        """Returns the current movement action.

        Returns:
            str: 'run', 'walk', or 'idle'.
        """
        if self.orientation.x != 0 or self.orientation.z != 0:
            if self.speed_control > 1:
                return 'run'
            return 'walk'

        return 'idle'
