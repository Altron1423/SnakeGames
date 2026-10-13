from dataclasses import dataclass

from libs.math import Position2, Vector2


@dataclass
class AttributeLayerEntityDTO:
    """Data Transfer Object for attribute layers of an entity.

    Attributes:
        constitution (int): Constitution attribute.
        agility (int): Agility attribute.
        defense (int): Defense attribute.
        strength (int): Strength attribute.
        intellect (int): Intellect attribute.
        spirit (int): Spirit attribute.
        health_reg (int): Health regeneration.
        max_mana (int): Maximum mana.
    """
    constitution: int = 0
    agility: int = 0
    defense: int = 0
    strength: int = 0
    intellect: int = 0
    spirit: int = 0
    health_reg: int = 0
    max_mana: int = 0

    def __add__(self, other: "AttributeLayerEntityDTO"):
        """Adds two attribute layer DTOs.

        Args:
            other (AttributeLayerEntityDTO): The other attribute layer DTO to add.

        Returns:
            AttributeLayerEntityDTO: A new DTO with summed attributes.
        """
        return AttributeLayerEntityDTO(
            constitution=   self.constitution + other.constitution,
            agility=        self.agility + other.agility,
            defense=        self.defense + other.defense,
            strength=       self.strength + other.strength,
            intellect=      self.intellect + other.intellect,
            spirit=         self.spirit + other.spirit,
            health_reg=     self.health_reg + other.health_reg,
            max_mana=       self.max_mana + other.max_mana
        )

    def __mul__(self, other: "AttributeLayerEntityDTO"):
        """Multiplies two attribute layer DTOs.

        Args:
            other (AttributeLayerEntityDTO): The other attribute layer DTO to multiply by.

        Returns:
            AttributeLayerEntityDTO: A new DTO with multiplied attributes.
        """
        return AttributeLayerEntityDTO(
            constitution=   int(self.constitution * other.constitution),
            agility=        int(self.agility * other.agility),
            defense=        int(self.defense * other.defense),
            strength=       int(self.strength * other.strength),
            intellect=      int(self.intellect * other.intellect),
            spirit=         int(self.spirit * other.spirit),
            health_reg=     int(self.health_reg * other.health_reg),
            max_mana=       int(self.max_mana * other.max_mana)
        )


@dataclass
class EntityToClientDTO:
    """Data Transfer Object for entity information sent to the client.

    Attributes:
        name (str): Name of the entity.
        id (int): Unique identifier of the entity.
        position (Position2): Current position of the entity.
        health ("ProgressBar"): Health status of the entity.
        orientation (Vector2): Orientation vector of the entity.
        visual_action (str): Current visual action or animation state.
    """
    name: str
    id: int
    position: Position2
    health: "ProgressBar"
    orientation: Vector2
    visual_action: str
