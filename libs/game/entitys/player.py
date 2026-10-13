from libs.dtos import ClientPlayerDTO, GameDataToServerDTO, GameDataToClientDTO, PlayerLoadDTO
from libs.game.sub_classes import Inventory
from libs.math import Position2
from .entity import Entity


class Player(Entity):
    """Represents a player in the game.

    Inherits from the Entity class and includes player-specific properties like inventory.
    """
    inventory: Inventory

    def __init__(self):
        """Initializes a new Player instance."""
        super().__init__()
        self.inventory = Inventory()

    def set_default(self, name: str, spawn_position: Position2):
        """Sets the initial name and spawn position for the player.

        Args:
            name (str): The player's name.
            spawn_position (Position2): The initial position.
        """
        self.name = name
        self.position = spawn_position

    def set_changes_from_client(self, dto: GameDataToServerDTO):
        """Updates the player's state based on client input.

        Args:
            dto (GameDataToServerDTO): The data received from the client.
        """
        if abs(dto.move.x) + abs(dto.move.z) <= 2.2:
            self.orientation = dto.move
        self.speed_control = dto.speed

    def get_data_for_client(self) -> GameDataToClientDTO:
        """Prepares player data for transmission to the client.

        Returns:
            GameDataToClientDTO: The DTO containing player-related data.
        """
        dto = GameDataToClientDTO(
            map_block="",
            entities=self.map_block.get_entity_dto(),
            player=self.__player_data__,
            chunk_position=Position2(0, 0),
            position=self.position
        )
        return dto

    def disconnect(self):
        """Removes the player from the current map block."""
        self.map_block.players_in_game.remove(self)

    def connect(self):
        """Adds the player to the current map block."""
        self.map_block.players_in_game.append(self)

    def get_near_entity(self, max_range: int) -> dict[str, int]:
        """Retrieves nearby entities within a certain range.

        Args:
            max_range (int): The maximum distance to search.

        Returns:
            dict[str, int]: A dictionary of entity names and their IDs.
        """
        return self.map_block.get_near_entity(self.name, max_range)

    @classmethod
    def load_from_config(cls, dto: PlayerLoadDTO) -> "Player":
        """Loads a player from a provided configuration DTO.

        Args:
            dto (PlayerLoadDTO): The DTO containing player configuration.

        Returns:
            Player: The loaded player instance.
        """
        player = super().load_from_config(dto)

        return player

    @property
    def __player_data__(self) -> ClientPlayerDTO:
        """Prepares player data for client-side representation.

        Returns:
            ClientPlayerDTO: The DTO containing player data.
        """
        return ClientPlayerDTO(
            name=self.name,
            id=self.id,
            attributes=self.attributes.__dict__(),
            position=self.position,
            health=self.health,
            mana=self.mana,
            xp=self.xp,
            lvl=self.lvl,
            inventory=str(self.inventory),
            map_block=self.map_block.name
        )

    def __copy__(self) -> "Player":
        """Creates a copy of the player.

        Returns:
            Player: A copy of the player.
        """
        player = super().__copy__()
        player.inventory = self.inventory
        return player
