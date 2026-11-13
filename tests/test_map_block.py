import unittest
from libs.save.map_block import MapBlock, MapChunk
from libs.math import Size2, Position2


class MapBlockTestCase(unittest.TestCase):
    def test_add_fruit(self):
        map_block = MapBlock(Size2(3, 3), "test")
        map_block.generator_x = lambda a, b: 0
        map_block.generator_y = lambda a, b: 0
        for i in range(9):
            map_block.set_chunk_on(MapChunk(f"{i}", Size2(3, 3)), Position2(i % 3, i // 3))

        map_block.create_fruit()
        self.assertEqual(map_block.get_chunk(Position2(0,0)).get_fruit_count, 1)

        map_block.create_fruit()
        self.assertEqual(map_block.get_chunk(Position2(0,0)).get_fruit_count, 2)

        self.assertEqual(map_block.get_chunk(Position2(1,0)).get_fruit_count, 0)

        self.assertEqual(map_block.get_chunk(Position2(0,1)).get_fruit_count, 0)

        map_block.create_fruit()
        self.assertEqual(map_block.get_chunk(Position2(0,0)).get_fruit_count, 2)

        self.assertEqual(map_block.get_chunk(Position2(1,0)).get_fruit_count, 1)

        self.assertEqual(map_block.get_chunk(Position2(0,1)).get_fruit_count, 0)


if __name__ == '__main__':
    unittest.main()
