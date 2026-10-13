from time import time
from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class TimerDTO:
    """Data class representing a timer's properties.

    Attributes:
        name (str):               название таймера.
        activation_time (int):    время активации.
        function (Callable):      запускаемая функция.
        data_for_function (Any):  дополнительная информация, передаваемая в функцию при запуске.
    """
    name: str
    activation_time: int
    function: Callable
    data_for_function: Any


class Timers:
    """Manages a collection of timers to be executed at specific times.

    Attributes:
        timers (list[TimerDTO]): A list of currently active timers.
        rate (int): The interval (in seconds) between timer updates.
        next_update (float): The timestamp of the next scheduled update.
    """
    timers: list[TimerDTO]
    rate: int
    next_update: float

    def __init__(self, rate: int = 1):
        """Initializes the Timers manager.

        Args:
            rate (int): The interval (in seconds) between timer updates.
        """
        self.timers = []
        self.rate = rate
        self.next_update = time()

    def add(self, timer: TimerDTO | dict):
        """Adds a new timer to the manager.

        Args:
            timer (TimerDTO | dict): Either a TimerDTO instance or a dictionary
                                     containing timer properties.
        """
        if isinstance(timer, dict):
            timer = TimerDTO(
                name=timer["name"],
                activation_time=time() + timer["activation_time"],
                function=timer["function"],
                data_for_function=timer["data_for_function"]
            )
        self.timers.append(timer)

    def update(self):
        """Checks and executes timers that have reached their activation time.

        Updates the next scheduled update time based on the rate.
        """
        if self.next_update <= time():
            self.next_update += self.rate
            remaining_timers = []
            for t in self.timers:
                if t.activation_time <= time():
                    t.function(t.data_for_function)
                else:
                    remaining_timers.append(t)
            self.timers = remaining_timers
