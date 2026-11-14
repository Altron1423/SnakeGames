import unittest
from pathlib import Path
from file_works.compilator import Compilator


class CompilatorTestCase(unittest.TestCase):
    def test_compiling_1(self):
        compilator = Compilator(
            Path() / "result_program.txt"
        )
        compilator.compile(Path() / "test_program.txt")
        with (Path.cwd() / "result_program.txt").open("r", encoding="utf-8") as f:
            self.assertEqual(
                f.read(),
                """
Grass = 1
Wall = 2
Fruit = 3

def run(snake, map):
     os
    snake.Right()
    return
    snake.Left()
    return
    map.TypeBlock()
    Wool
    Grass
    Fruit
    snake_u = "TOP"
    if map.PosInfo(0, 1) == Wool:
        snake.Right()
        return
    (print(1))""")  # add assertion here


if __name__ == '__main__':
    unittest.main()
