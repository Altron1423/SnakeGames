import json
from pathlib import Path

from libs import MapChunkConfigMapper
from libs.save.map_chunk import MapChunk
from libs.loaders.loader import Loader
from libs.loaders.map_plate_loader import map_plate_loader
from libs.math import Size2


class MapChunkLoader(Loader):
    """A loader class for map chunks.

    This class is responsible for loading map chunk data from files.
    """
    elements: dict[str, MapChunk]

    def load(self, path: Path) -> None:
        """Loads a map chunk from a specified path.

        Args:
            path (Path): The path to the file containing map chunk data.
        """
        with path.open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "map_chunk":
                data = MapChunkConfigMapper.dict_to_dto(json_data["data"])
                size = Size2(data.size)
                map_chunk = MapChunk(data.name, size)
                map_chunk.height_map = data.height_map
                plates = data.map_plates

                get_plate = lambda position: data.plates[str(plates[position.z][position.x])]
                for position in size:
                    map_chunk.set_plate_on(
                        map_plate_loader.get_changeable(
                            get_plate(position),
                        ),
                        position
                    )

                self.add(map_chunk, data.name)

    def get(self, name: str) -> MapChunk | None:
        """Retrieves a loaded map chunk by name.

        Args:
            name (str): The name of the map chunk.

        Returns:
            MapChunk | None: The map chunk object if found, otherwise None.
        """
        element = self.elements.get(name)
        return element

    def get_new(self, name: str) -> MapChunk | None:
        """Retrieves a copy of a loaded map chunk by name.

        Args:
            name (str): The name of the map chunk.

        Returns:
            MapChunk | None: A copy of the map chunk object.
        """
        element = self.elements.get(name).__copy__()
        return element


map_chunk_loader = MapChunkLoader()
