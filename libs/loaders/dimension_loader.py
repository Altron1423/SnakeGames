import json
from pathlib import Path

from libs import loger, DimensionConfigMapper
from libs.save.dimension import Dimension
from libs.loaders import Loader
from libs.loaders import map_block_loader
from libs.math import Size2


class DimensionLoader(Loader):
    """A loader class for dimensions.

    This class is responsible for loading dimension data from files.
    """
    elements: dict[str, Dimension]

    def load(self, path: Path) -> None:
        """Loads a dimension from a specified path.

        Args:
            path (Path): The path to the file containing dimension data.
        """
        with Path(path).open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "dimension":
                data = DimensionConfigMapper.dict_to_dto(json_data["data"])
                size = Size2(data.size)
                dimension = Dimension(size, data.name)

                for block_name in data.blocks:
                    if map_block_loader.get(block_name):
                        dimension.add_using_block(block_name)

                self.add(dimension, data.name)

    def load_from_dir(self, path: Path) -> None:
        """Loads all dimensions from a directory.

        Args:
            path (Path): The directory containing dimension files.
        """
        for iPath in path.iterdir():
            loger.log(f"Loading {iPath}")
            self.load(iPath)

    def get(self, name: str) -> Dimension | None:
        """Retrieves a loaded dimension by name.

        Args:
            name (str): The name of the dimension.

        Returns:
            Dimension | None: The dimension object if found, otherwise None.
        """
        return super().get(name)

    def get_new(self, name: str) -> Dimension | None:
        """Retrieves a dimension or returns a new one if not found.

        Args:
            name (str): The name of the dimension.

        Returns:
            Dimension | None: The dimension object.
        """
        return super().get_new(name)


dimension_loader = DimensionLoader()
