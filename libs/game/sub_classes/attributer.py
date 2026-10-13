from json import loads, dumps
from libs.dtos.entity import AttributeLayerEntityDTO
from libs.mappers.entity import AttributeLayerEntityMapper


class Attributer:
    """Manages an entity's attributes using multiple layers.

    The final attributes are calculated by summing the values from basic,
    elevated, artefact, and effect layers, then multiplying by a ratio.
    """
    _type_: str = "Attributer"

    _basic: AttributeLayerEntityDTO
    _elevated: AttributeLayerEntityDTO
    _artefacts: AttributeLayerEntityDTO
    _effects: AttributeLayerEntityDTO
    _ratio: AttributeLayerEntityDTO
    result: AttributeLayerEntityDTO

    def __init__(self):
        """Initializes the Attributer with empty layers.
            constitution - телосложение
            agility - ловкость
            defense - защита
            strength - сила
            intellect - интеллект
            spirit - дух
            health_reg - здоровье
            max_mana - макс_мана
        """
        self._basic = AttributeLayerEntityDTO()
        self._elevated = AttributeLayerEntityDTO()
        self._artefacts = AttributeLayerEntityDTO()
        self._effects = AttributeLayerEntityDTO()
        self._ratio = AttributeLayerEntityDTO()
        self.result = AttributeLayerEntityDTO()

    def save(self):
        """Placeholder for saving attributes.

        Note: This is currently a stub.
        """
        ...

    def load_from_str(self, data: str):
        """Loads attributes from a serialized string.

        The expected format is '<Attributer_JSON_data>'.

        Args:
            data (str): The serialized attribute string.

        Raises:
            TypeError: If the string format is incorrect or type doesn't match.
        """
        if data[0] == '<' and data[-1] == '>':
            data = data[1:-1]
            tp, data = data.split('_')
            if tp != self._type_:
                raise TypeError(f"This string not {self._type_}")
            self.load(loads(data))
        else:
            raise TypeError("Attributer only accepts strings")

    def load(self, data: dict[str, list[int | float]]):
        """Loads attributes from a dictionary of attribute lists.

        Args:
            data (dict[str, list[int | float]]): Dictionary containing attribute layers.
        """
        if "basic" in data:
            self._basic = AttributeLayerEntityMapper.list_to_dto(data["basic"])
        if "elevated" in data:
            self._elevated = AttributeLayerEntityMapper.list_to_dto(data["elevated"])
        if "artefacts" in data:
            self._artefacts = AttributeLayerEntityMapper.list_to_dto(data["artefacts"])
        if "effects" in data:
            self._effects = AttributeLayerEntityMapper.list_to_dto(data["effects"])
        if "ratio" in data:
            self._ratio = AttributeLayerEntityMapper.list_to_dto(data["ratio"])

    def update(self):
        """Recalculates the final result attribute using the layers and ratio."""
        self.result = (self._basic + self._elevated + self._artefacts + self._effects) * self._ratio

    @property
    def constitution(self) -> int:
        """Gets the constitution attribute."""
        return self.result.constitution

    @property
    def agility(self) -> int:
        """Gets the agility attribute."""
        return self.result.agility

    @property
    def defense(self) -> int:
        """Gets the defense attribute."""
        return self.result.defense

    @property
    def strength(self) -> int:
        """Gets the strength attribute."""
        return self.result.strength

    @property
    def intellect(self) -> int:
        """Gets the intellect attribute."""
        return self.result.intellect

    @property
    def spirit(self) -> int:
        """Gets the spirit attribute."""
        return self.result.spirit

    @property
    def health_reg(self) -> int:
        """Gets the health regeneration attribute."""
        return self.result.health_reg

    @property
    def max_mana(self) -> int:
        """Gets the maximum mana attribute."""
        return self.result.max_mana

    def __dict__(self):
        """Returns a dictionary representation of the attribute layers.

        Returns:
            dict: Dictionary containing layers 'basic', 'elevated', 'artefacts', 'effects', and 'ratio'.
        """
        return {
            "basic": AttributeLayerEntityMapper.dto_to_list(self._basic),
            "elevated": AttributeLayerEntityMapper.dto_to_list(self._elevated),
            "artefacts": AttributeLayerEntityMapper.dto_to_list(self._artefacts),
            "effects": AttributeLayerEntityMapper.dto_to_list(self._effects),
            "ratio": AttributeLayerEntityMapper.dto_to_list(self._ratio),
        }

    def __str__(self):
        """Returns a string representation of the Attributer."""
        return f"<{self._type_}_{dumps(self.__dict__(), separators=(',', ':'))}>"
