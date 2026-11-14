from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from typing import Callable


class Compilator:
    path:           Path | None
    target_path:    Path

    commands: dict
    constants: dict
    function: Callable

    def __init__(self, target_path: Path):
        self.path = None
        self.target_path = target_path
        self.commands = {
            "TypeBlock()": "map.TypeBlock()"
        }
        self.constants = {
            "Grass": 1,
            "Wall": 2,
            "Fruit": 3,
        }
        self.default_code_block = """
Grass = {Grass}
Wall = {Wall}
Fruit = {Fruit}

def run(snake, map):""".format(**self.constants)
        print(target_path)
        if not target_path.is_file():
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with target_path.open("a", encoding="utf-8") as file:
                file.write(
                    self.default_code_block
                    +
                    "\n    pass"
                )

    def compile(self, path: Path):
        self.path = path
        self._compile()

    def load(self):
        name = "compiling_code"
        path = str(self.target_path.resolve())
        spec = spec_from_file_location(name, path)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.function = mod.run
        return self.function


    def _compile(self):
        if self.path is None or self.target_path is None:
            return
        text = self.default_code_block
        with self.path.open("r", encoding="utf-8") as file:
            for raw_line in file.readlines():
                lines = self._cleen_line(raw_line)
                text += "".join(["\n    " + line for line in lines])
            text += "\n    ..."
        with self.target_path.open("w", encoding="utf-8") as file:
            file.write(text)

    def _cleen_line(self, line: str) -> list[str]:
        line = line.replace("\n", "")
        if "#" in line:
            line = line.split("#")[0]

        line = line.replace("import ", " ")
        line = line.replace("exec(", "(")

        line = line.replace("snake", "snake_u")
        line = line.replace("map", "map_u")
        line = line.replace("PosInfo(", "map.PosInfo(")

        i = 0
        while i < len(line):
            if line[i] == " ":
                i += 1
            else:
                shift = " " * i
                line  = line[i:]
                break
        else:
            return []

        line = line.strip(" ")

        if line.find("Right()") != -1:
            line = line.replace("Right()", "snake.Right()")
            lines = [f"{shift}{line}", f"{shift}return"]
        elif line.find("Left()") != -1:
            line = line.replace("Left()", "snake.Left()")
            lines = [f"{shift}{line}", f"{shift}return"]
        else:
            lines = [f"{shift}{line}"]

        return lines

if __name__ == "__main__":
    compilator = Compilator(
        Path() / "tests/result_program.txt"
    )
    compilator.compile(Path() / "tests/test_program.txt")
