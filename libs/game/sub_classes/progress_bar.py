from dataclasses import dataclass
from typing import Callable, Any

from ..exception import BarReadSrtException

@dataclass
class TriggersDTO:
    """A data class to hold callback functions for bar events.

    Attributes:
        _min_limit (Callable[..., Any] | None): Callback when the bar reaches its minimum limit.
        _below_zero (Callable[..., Any] | None): Callback when the bar value goes below zero.
        _above_zero (Callable[..., Any] | None): Callback when the bar value goes above zero.
        _limit (Callable[..., Any] | None): Callback when the bar reaches its maximum limit.
        _increasing (Callable[..., Any] | None): Callback when the bar value increases.
        _decreasing (Callable[..., Any] | None): Callback when the bar value decreases.
    """
    _min_limit:  Callable[..., Any] | None = None
    _below_zero: Callable[..., Any] | None = None
    _above_zero: Callable[..., Any] | None = None
    _limit:      Callable[..., Any] | None = None
    _increasing: Callable[..., Any] | None = None
    _decreasing: Callable[..., Any] | None = None

    def min_limit(self):
        """Triggers the minimum limit callback if it exists."""
        if self._min_limit:
            self._min_limit()

    def below_zero(self):
        """Triggers the below zero callback if it exists."""
        if self._below_zero:
            self._below_zero()

    def above_zero(self):
        """Triggers the above zero callback if it exists."""
        if self._above_zero:
            self._above_zero()

    def limit(self):
        """Triggers the limit callback if it exists."""
        if self._limit:
            self._limit()

    def increasing(self):
        """Triggers the increasing callback if it exists."""
        if self._increasing:
            self._increasing()

    def decreasing(self):
        """Triggers the decreasing callback if it exists."""
        if self._decreasing:
            self._decreasing()


class ProgressBar:
    """A progress bar with value, limit, minimum limit, and unlimit capabilities.

    Attributes:
        trigger_check (bool): Whether to check triggers on update.
        value (int): Current value.
        limit (int): Maximum value.
        min_limit (int): Minimum value.
        unlimit (bool): Whether the bar has no limit.
        triggers (TriggersDTO | None): Callbacks to trigger on value changes.
        below_zero (bool): Flag indicating if the value is below zero.
        _type_ (str): The type name of the object.
    """
    trigger_check: bool = True
    value: int
    limit: int
    min_limit: int
    unlimit: bool
    triggers: TriggersDTO = None
    below_zero: bool
    _type_: str = "ProgressBar"

    def __init__(self, value: int = 1, limit: int = 100, min_value: int = 0, unlimit: bool = False):
        """Initializes the ProgressBar.

        Args:
            value (int): Initial value.
            limit (int): Initial limit.
            min_value (int): Initial minimum value.
            unlimit (bool): If True, the bar has no limit.
        """
        if type(value) in [list, tuple]:
            self.value, self.limit = value
        else:
            self.value = value
            self.limit = limit
        self.min_limit = min_value
        self.unlimit = unlimit
        self.below_zero = False

    @classmethod
    def init_from_str(cls, data: str):
        """Creates a ProgressBar from a serialized string.

        The format expected is '<ProgressBar:min/val/limit>'.

        Args:
            data (str): The serialized string.

        Returns:
            ProgressBar: A new ProgressBar instance.

        Raises:
            BarReadSrtException: If the string format is invalid.
        """
        if data[0] == '<' and data[-1] == '>':
            data = data[1:-1]
            tp, data = data.split(':')
            if tp != cls._type_:
                raise BarReadSrtException(f"This string not {cls._type_}")
            data = list(map(int, data.split("/")))
            return cls(data[1], data[2], data[0])
        else:
            raise BarReadSrtException("Bar only accepts strings")

    def set_triggers(self, triggers: TriggersDTO):
        """Sets the triggers for the progress bar.

        Args:
            triggers (TriggersDTO): The triggers object.
        """
        self.triggers = triggers

    def trigger_activ(self, increase: bool):
        """Triggers relevant callbacks based on value change.

        Args:
            increase (bool): True if value increased, False if decreased.
        """
        if self.trigger_check and self.triggers:
            if increase:
                if self.value >= self.limit:
                    if not self.unlimit:
                        self.value = self.limit
                    self.triggers.limit()
                if self.value >= 0 and self.below_zero:
                    self.below_zero = False
                    self.triggers.above_zero()
                self.triggers.increasing()
            else:
                if self.value <= self.min_limit:
                    if not self.unlimit:
                        self.value = self.min_limit
                    self.triggers.min_limit()
                if self.value <= 0 and self.below_zero == False:
                    self.below_zero = True
                    self.triggers.below_zero()
                self.triggers.decreasing()

    def update(self, value=0, limit=100):
        """Updates the value and limit of the progress bar.

        Args:
            value: New value (int, list, or tuple).
            limit: New limit (int, list, or tuple).
        """
        before = self.value
        if type(value) in [list, tuple]:
            self.value, self.limit = value
        else:
            self.value = value
            self.limit = limit
        self.trigger_activ((self.value - before) > 0)

    def get_full(self, from_zero=False):
        """Returns the current value and limit.

        Args:
            from_zero (bool): If True, returns (value, limit).
                               If False, returns (value - min_limit, limit - min_limit).

        Returns:
            tuple: A tuple containing (value, limit).
        """
        if from_zero:
            return self.value, self.limit
        else:
            return self.value - self.min_limit, self.limit - self.min_limit

    def __add__(self, dat: int):
        """Adds a value to the progress bar.

        Args:
            dat (int): The value to add.

        Returns:
            ProgressBar: The updated progress bar.
        """
        dat = int(dat)
        self.value += dat
        self.trigger_activ(dat > 0)
        return self

    def set_value(self, dat: int):
        """Sets a new value for the progress bar.

        Args:
            dat (int): The new value.
        """
        old_value = self.value
        self.value = int(dat)
        self.trigger_activ((self.value - old_value) > 0)

    def add_limit(self, dat: int):
        """Increases the limit of the progress bar.

        Args:
            dat (int): The amount to increase the limit by.
        """
        self.limit += int(dat)
        self.trigger_activ(True)

    def set_limit(self, dat: int):
        """Sets a new limit for the progress bar.

        Args:
            dat (int): The new limit.
        """
        self.limit = int(dat)
        self.trigger_activ(True)

    def add_min_limit(self, dat: int):
        """Increases the minimum limit of the progress bar.

        Args:
            dat (int): The amount to increase the minimum limit by.
        """
        self.min_limit += int(dat)
        self.trigger_activ(False)

    def set_min_limit(self, dat: int):
        """Sets a new minimum limit for the progress_bar.

        Args:
            dat (int): The new minimum limit.
        """
        self.min_limit = int(dat)
        self.trigger_activ(False)

    def __str__(self):
        """Returns a string representation of the progress bar.

        Returns:
            str: A string in the format '<ProgressBar:min/val/limit>'.
        """
        return f"<{self._type_}:{self.min_limit}/{self.value}/{self.limit}>"

    def __copy__(self, with_triggers: bool = False):
        """Creates a copy of the progress bar.

        Args:
            with_triggers (bool): If True, copies the triggers object.

        Returns:
            ProgressBar: A copy of the progress bar.
        """
        bar = ProgressBar(self.value, self.limit, self.min_limit, self.unlimit)
        if with_triggers:
            bar.set_triggers(self.triggers)
        return bar
