from typing import Callable
import pygame as pg
from pathlib import Path
from libs.Core import CORE
from libs.Loger import loger
import src.modules.screen as screen
from libs.math import Size2
from libs.ticker import Ticker, MainTicker


class Application:
    """Base class for the game application.

    Manages the main game loop, event handling, and system-wide functions.

    Attributes:
        clock (pg.time.Clock): Pygame clock for managing frame rate.
        TPS (int): Ticks per second.
        tick (Ticker): Ticker object for game logic timing.
        path (Path): The current working directory.
        WORK (bool): Flag indicating if the application is running.
        main_screen (screen.MainScreen): The primary screen manager.
        function_runs (dict): A registry of functions that can be called.
    """

    clock: pg.time.Clock
    TPS: int
    tick: Ticker
    path: Path
    WORK: bool
    main_screen: screen.MainScreen
    function_runs: dict[str, dict[str, list[Callable[..., None] | None]]]

    def __init__(self):
        """Initializes the application, setting up screens and parameters."""
        loger.status("App init started")

        self._set_start_parameters()

        self.main_screen = screen.MainScreen(self)
        self.window_manager = self.main_screen.window_manager

        self._create_functions_dict()

        loger.status("App init complete")
        loger.pass_line(2)

    def run(self):
        """Starts the main application loop."""
        loger.status("App start")
        try:
            while self.WORK:
                self.tick.tick()
                self.clock.tick(self.TPS)

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.exit(None)
                    elif event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                        self.main_screen.window_manager.key_press(event.key, event.type)
                        self.key_press(event.key, event.type == pg.KEYDOWN)
                    elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                        self.main_screen.window_manager.select(event)
                    elif event.type == pg.VIDEORESIZE:
                        self.main_screen.resize_main_screen(Size2(event.size))

                self.main_screen.draw()
                self.run_more()
        except KeyboardInterrupt:
            self.exit()

    def key_press(self, key: str, key_down: bool):
        """Handles key press and release events.

        Args:
            key (str): The key that was pressed or released.
            key_down (bool): True if the key was pressed, False if released.
        """
        ...

    def run_more(self):
        """Executes periodic tasks or secondary loops."""
        ...

    def exit(self, _=None):
        """Exits the application cleanly."""
        self.WORK = False
        loger.log("App exit")

    def _set_start_parameters(self):
        """Sets initial application parameters."""
        self.clock = pg.time.Clock()
        self.TPS = 30
        self.tick = MainTicker
        self.path = Path.cwd()
        self.WORK = True

        loger.status(f"App version: {CORE.version}")
        loger.status("Set App parameters complete")

    def _create_functions_dict(self):
        """Initializes the function registry for system and mods."""
        sist = {
            "exit": [self.exit, None]
        }
        self.function_runs = {"sistem": sist, "mods": {}}

        loger.status("Function giver generate complete")

    def add_functions(self, dict_functions: dict):
        """Adds new functions to the application's registry.

        Args:
            dict_functions (dict): A dictionary where keys are categories and
                values are dictionaries mapping function names to a list [function, None].
        Example:
            {"key": {"name": [lambda x: print(1), None]}}
        """
        for key, functions in dict_functions.items():
            if key != "sistem":
                if key not in self.function_runs:
                    self.function_runs[key] = {}
                for name, function in functions.items():
                    self.function_runs[key][name] = function

    def give_function(self, data, passw=None):
        """Retrieves a function from the registry based on the provided path.

        Args:
            data (list | dict): The path to the function in the registry.
            passw (any, optional): Password required if the function requires one.

        Returns:
            dict: A dictionary containing the result and either the function or an error message.
        """
        m: dict | list = self.function_runs
        for i in data:
            if i in m:
                m = m[i]
            else:
                return {"result": False, "error": [0, f"{i} from {data} undefined"]}
        if type(m) == dict:
            return {"result": False, "error": [1, f"{data} is unfull address"]}
        elif m[1] == passw:
            return {"result": True, "function": m[0]}
        else:
            return {"result": False, "error": [3, f"uncorrect passw"]}
