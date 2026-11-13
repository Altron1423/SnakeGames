import unittest
from pathlib import Path
from file_works.compilator import Compilator


class CompilatorTestCase(unittest.TestCase):
    def test_compiling_1(self):
        compilator = Compilator(
            Path.cwd() / "test_program.txt",
            Path.cwd() / "result_program.txt"
        )
        with (Path.cwd() / "result_program.txt").open("r", encoding="utf-8") as f:
            self.assertEqual(
                f.read(),
                """
Grass = 0
Wool = 1
Fruit = 2

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
    if map.TypeBlock() == Wool:
        snake.Right()
        return
    (print(1))""")  # add assertion here


if __name__ == '__main__':
    unittest.main()
