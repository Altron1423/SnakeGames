from pathlib import Path


class Compilator:
    path:           Path
    target_path:    Path

    commands: dict

    def __init__(self, path: Path, target_path: Path):
        self.path = path
        self.target_path = target_path
        self.commands = {
            "TypeBlock()": "map.TypeBlock()"
        }
        self._compile()

    def _compile(self):
        text = """
Grass = 0
Wool = 1
Fruit = 2

def run(snake, map):"""
        with self.path.open("r", encoding="utf-8") as file:
            for raw_line in file.readlines():
                lines = self._cleen_line(raw_line)
                text += "".join(["\n    " + line for line in lines])
        with self.target_path.open("w", encoding="utf-8") as file:
            file.write(text)

    def _cleen_line(self, line: str) -> list[str]:
        line = line.replace("\n", "")
        if "#" in line:
            line = line.split("#")[0]

        line = line.replace("import ", " ")
        line = line.replace("exec(", "(")

        line = line.replace("TypeBlock(", "map.TypeBlock(")

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
        Path("/") / "tests/test_program.txt",
        Path("/") / "tests/result_program.txt"
    )
