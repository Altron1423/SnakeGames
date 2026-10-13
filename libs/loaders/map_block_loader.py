import json
from pathlib import Path

from libs import MapBlockConfigMapper
from libs.save.map_block import MapBlock
from libs.loaders import map_chunk_loader
from libs.loaders import Loader
from libs.math import Size2


class MapBlockLoader(Loader):
    """A loader class for map blocks.

    This class is responsible for loading map block data from files.
    """
    elements: dict[str, MapBlock]

    def load(self, path: Path) -> None:
        """Loads a map block from a specified path.

        Args:
            path (Path): The path to the file containing map block data.
        """
        with path.open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "map_block":
                data = MapBlockConfigMapper.dict_to_dto(json_data["data"])
                size = Size2(data.size)
                map_block = MapBlock(
                    size,
                    data.name
                )

                form = data.form
                for position in size:
                    if form[position.z][position.x] is not None:
                        map_block.set_chunk_on(
                            map_chunk_loader.get(
                                form[position.z][position.x],
                            ),
                            position
                        )
                self.add(map_block, data.name)

    def get(self, name: str) -> MapBlock | None:
        """Retrieves a loaded map block by name.

        Args:
            name (str): The name of the map block.

        Returns:
            MapBlock | None: The map block object if found, otherwise None.
        """
        return super().get(name)

    def get_new(self, name: str) -> MapBlock | None:
        """Retrieves a map block or returns a new one if not found.

        Args:
            name (str): The name of the map block.

        Returns:
            MapBlock | None: The map block object.
        """
        return super().get_new(name)


map_block_loader = MapBlockLoader()
