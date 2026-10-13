from typing import Any, Callable
import pygame as pg


KeysTransf = {
    pg.K_q: "q", pg.K_w: "w", pg.K_e: "e", pg.K_r: "r", pg.K_t: "t", pg.K_y: "y",
    pg.K_u: "u", pg.K_i: "i", pg.K_o: "o", pg.K_p: "p", pg.K_a: "a", pg.K_s: "s",
    pg.K_d: "d", pg.K_f: "f", pg.K_g: "g", pg.K_h: "h", pg.K_j: "j", pg.K_k: "k",
    pg.K_l: "l", pg.K_z: "z", pg.K_x: "x", pg.K_c: "c", pg.K_v: "v", pg.K_b: "b",
    pg.K_n: "n", pg.K_m: "m", pg.K_0: "0", pg.K_1: "1", pg.K_2: "2", pg.K_3: "3",
    pg.K_4: "4", pg.K_5: "5", pg.K_6: "6", pg.K_7: "7", pg.K_8: "8", pg.K_9: "9",
    pg.K_SPACE: " ", pg.K_COMMA: ",", pg.K_PERIOD: ".", pg.K_SLASH: "/", pg.K_MINUS: "-"
}

KeysTransfRevers = {v: k for k, v in KeysTransf.items()}


class TriggerGen:
    """A builder for creating event triggers for UI elements.

    Triggers are stored in a dictionary where keys are tuples of (event_identifier, state).
    Event identifiers can be integers (for mouse buttons/keys) or strings (for 'hold').
    States are booleans (True for 'down', False for 'up').

    Attributes:
        triggers (dict): A mapping from (event_identifier, state) to a callback function.
        last (tuple | None): The last key accessed in the triggers dictionary.
    """

    triggers: dict[tuple[str, bool] | tuple[int, bool], Callable[["Button"], Any]]

    def __init__(self):
        """Initializes an empty TriggerGen object."""
        self.triggers = {}
        self.last = None

    def LMD(self, function: Callable[["Button"], Any]) -> "TriggerGen":
        """Sets a trigger for Left Mouse Down.

        Args:
            function (Callable): The callback to execute.

        Returns:
            TriggerGen: The current instance (for chaining).
        """
        self.triggers[(1, True)] = function
        return self

    def LMU(self, function: Callable[["Button"], Any]) -> "TriggerGen":
        """Sets a trigger for Left Mouse Up.

        Args:
            function (Callable): The callback to execute.

        Returns:
            TriggerGen: The current instance (for chaining).
        """
        self.triggers[(1, False)] = function
        return self

    def RMD(self, function: Callable[["Button"], Any]) -> "TriggerGen":
        """Sets a trigger for Right Mouse Down.

        Args:
            function (Callable): The callback to execute.

        Returns:
            TriggerGen: The current instance (for chaining).
        """
        self.triggers[(3, True)] = function
        return self

    def RMU(self, function: Callable[["Button"], Any]) -> "TriggerGen":
        """Sets a trigger for Right Mouse Up.

        Args:
            function (Callable): The callback to execute.

        Returns:
            TriggerGen: The current instance (for chaining).
        """
        self.triggers[(3, False)] = function
        return self

    def MWD(self, function: Callable[["Button"], Any]) -> "TriggerGen":
        """Sets a trigger for Middle Mouse Down.

        Args:
            function (Callable): The callback to execute.

        Returns:
            TriggerGen: The current instance (for chaining).
        """
        self.triggers[(4, False)] = function
        return self

    def MWU(self, function: Callable[["Button"], Any]) -> "TriggerGen":
        """Sets a trigger for Middle Mouse Up.

        Args:
            function (Callable): The callback to execute.

        Returns:
            TriggerGen: The current instance (for chaining).
        """
        self.triggers[(5, False)] = function
        return self

    def HoldD(self, function: Callable[["Button"], Any]) -> "TriggerGen":
        """Sets a trigger for holding a key down.

        Args:
            function (Callable): The callback to execute.

        Returns:
            TriggerGen: The current instance (for chaining).
        """
        self.triggers[('hold', True)] = function
        return self

    def HoldU(self, function: Callable[["Button"], Any]) -> "TriggerGen":
        """Sets a trigger for releasing a held key.

        Args:
            function (Callable): The callback to execute.

        Returns:
            TriggerGen: The current instance (for chaining).
        """
        self.triggers[('hold', False)] = function
        return self

    def key_down(self, key: int | str, function: Callable[["Button"], Any]) -> "TriggerGen":
        """Sets a trigger for a key press.

        Args:
            key (int | str): The pygame key constant or the string representation.
            function (Callable): The callback to execute.

        Returns:
            TriggerGen: The current instance (for chaining).
        """
        if isinstance(key, str):
            key = KeysTransfRevers.get(key)
        if key in KeysTransf:
            self.triggers[(key, True)] = function
        return self

    def key_up(self, key: int | str, function: Callable[["Button"], Any]) -> "TriggerGen":
        """Sets a trigger for a key release.

        Args:
            key (int | str): The pygame key constant or the string representation.
            function (Callable): The callback to execute.

        Returns:
            TriggerGen: The current instance (for chaining).
        """
        if isinstance(key, str):
            key = KeysTransfRevers.get(key)
        if key in KeysTransf:
            self.triggers[(key, False)] = function
        return self

    def __iadd__(self, other):
        """Merges another trigger object or dictionary into this one.

        Args:
            other (dict | TriggerGen): The trigger source to merge.

        Returns:
            TriggerGen: The current instance.
        """
        if isinstance(other, dict):
            for k, f in other.items():
                self.triggers[k] = f
        elif isinstance(other, self.__class__):
            for k, f in other.triggers.items():
                self.triggers[k] = f
        return self

    def __getitem__(self, key: tuple[str, bool] | tuple[int, bool]) -> Callable[["Button"], Any] | None:
            """Retrieves a trigger for the given key.

            Args:
                key (tuple): The key representing the event (identifier, state).

            Returns:
                Callable | None: The trigger function if found, otherwise None.
            """
            if key in self.triggers:
                self.last = key
                return self.triggers[key]
            return None
