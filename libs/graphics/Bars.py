class Bars:
    """A simple progress bar class.

    Attributes:
        TFupdate (bool): Whether to check and trigger events during updates.
        triggers (dict): A dictionary of callback functions. 
                         Keys can be: 'minL', 'zero', 'aZero', 'limit', 'upValue', 'downValue'.
        value (int/float): Current value.
        limit (int/float): Maximum value.
        minL (int/float): Minimum value.
        belowZero (bool): Flag indicating if the value is below zero.
    """
    TFupdate = True
    triggers: dict | None
    """
    triggers = {
        "minL": None, 
        "zero": None, 
        "aZero": None, 
        "limit": None, 
        "upValue": None, 
        "downValue": None
    }
    """

    def __init__(self, value=1, limit=100, minL=0, triggers=None):
        """Initializes the Bars object.

        Args:
            value (int | float | list | tuple): Initial value.
            limit (int | float): Initial limit.
            minL (int | float): Initial minimum limit.
            triggers (dict, optional): Initial dictionary of callbacks. Defaults to None.
        """
        if type(value) in [list, tuple]:
            self.value, self.limit = value
        else:
            self.value = value
            self.limit = limit
        self.minL = minL
        self.triggers = triggers
        self.belowZero = False

    def triggerActiv(self, dat):
        """Triggers relevant callbacks based on the change in value.

        Args:
            dat (float | int): The change in value (positive or negative).
        """
        if self.TFupdate:
            if dat < 0:
                if self.value <= self.minL:
                    self.value = self.minL
                    if self.value == 0 and "zero" in self.triggers:
                        self.triggers["zero"]()
                    if "minL" in self.triggers and self.triggers["minL"]:
                        self.triggers["minL"]()
                elif self.value <= 0 and not self.belowZero:
                    self.belowZero = True
                    if "zero" in self.triggers and self.triggers["zero"]:
                        self.triggers["zero"]()
                
                if "downValue" in self.triggers and self.triggers["downValue"]:
                    self.triggers["downValue"]()

            elif dat > 0:
                if self.value >= self.limit:
                    self.value = self.limit
                    if "limit" in self.triggers and self.triggers["limit"]:
                        self.triggers["limit"]()
                elif self.value >= 0 and self.belowZero:
                    self.belowZero = False
                    if "aZero" in self.triggers and self.triggers["aZero"]:
                        self.triggers["aZero"]()
                
                if "upValue" in self.triggers and self.triggers["upValue"]:
                    self.triggers["upValue"]()

    def update(self, value=0, limit=100):
        """Updates the value and limit of the bar.

        Args:
            value (int | float | list | tuple): New value or [value, limit] pair.
            limit (int | float): New limit.
        """
        before = self.value
        if type(value) in [list, tuple]:
            self.value, self.limit = value
        else:
            self.value = value
            self.limit = limit
        self.triggerActiv(self.value - before)

    def getFull(self, fromZero=False):
        """Returns the current value and limit.

        Args:
            fromZero (bool): If True, returns (value, limit).
                              If False, returns (value - minL, limit - minL).

        Returns:
            tuple: A tuple containing (value, limit).
        """
        if fromZero:
            return self.value, self.limit
        else:
            return self.value - self.minL, self.limit - self.minL

    def add(self, dat):
        """Adds a value to the current value.

        Args:
            dat (int | float): The value to add.
        """
        dat = int(dat)
        self.value += dat
        self.triggerActiv(dat)

    def setValue(self, dat: int | float):
        """Sets a new value for the bar.

        Args:
            dat (int | float): The new value.
        """
        old_value = self.value
        self.value = int(dat)
        self.triggerActiv(self.value - old_value)

    def addLimit(self, dat):
        """Increases the limit of the bar.

        Args:
            dat (int | float): The amount to increase the limit by.
        """
        self.limit += dat
        self.triggerActiv(dat)

    def setLimit(self, dat):
        """Sets a new limit for the bar.

        Args:
            dat (int | float): The new limit.
        """
        self.limit = dat
        self.triggerActiv(dat)

    def addMinLimit(self, dat):
        """Increases the minimum limit of the bar.

        Args:
            dat (int | float): The amount to increase the minimum limit by.
        """
        self.minL += dat
        self.triggerActiv(dat)

    def setMinLimit(self, dat):
        """Sets a new minimum limit for the bar.

        Args:
            dat (int | float): The new minimum limit.
        """
        self.minL = dat
        self.triggerActiv(dat)

    def __str__(self):
        """Returns a string representation of the bar.

        Returns:
            str: A string in the format 'value/limit'.
        """
        return f"{self.value}/{self.limit}"
