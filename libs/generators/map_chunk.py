from libs import MapChunk


class MapChunkGenerator:
    """A class for generating map chunks.

    This class provides static methods for generating various elements within a map chunk.
    """

    @staticmethod
    def gen1(map_chunk: MapChunk):
        """Generates content within a map chunk.

        Args:
            map_chunk (MapChunk): The map chunk to process.
        """
        for position in map_chunk.size:
            ...
        # print(map_chunk)
