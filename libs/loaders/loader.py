from pathlib import Path

file_packs = Path(__file__).resolve().parent.parent.parent
file_data = (file_packs / "src" / "data").resolve()
file_dop = (file_packs / "dop_assets").resolve()

class Loader:
    """Base class for loaders.

    Provides basic functionality for loading, storing, and retrieving elements.
    """
    elements: dict[str, object]
    global_load_data: dict[str, str] = {}

    def __init__(self):
        self.elements = {}

    def load(self, path: Path) -> None:
        """Loads elements from a file.

        Args:
            path (Path): The path to the file.
        """
        ...

    def load_from_dir(self, path: Path) -> None:
        """Loads elements from all files in a directory.

        Args:
            path (Path): The directory to load from.
        """
        if not path.is_dir():
            return
        for iPath in path.iterdir():
            self.load(iPath)

    def add(self, element: object, name: str, path: Path) -> None:
        """Adds an element to the storage.

        Args:
            element (object): The element to add.
            name (str): The name associated with the element.
        """
        self.elements[name] = element
        path = path.resolve()
        if path.is_relative_to(file_data):
            path = path.relative_to(file_data)
        elif path.is_relative_to(file_dop):
            path = path.relative_to(file_dop)

        self.global_load_data[name] = str(path)

    def get(self, name: str) -> object | None:
        """Retrieves an element by name.

        Args:
            name (str): The name of the element.

        Returns:
            object | None: The element if found, otherwise None.
        """
        element = self.elements.get(name)
        return element

    def get_changeable(self, name: str) -> object | None:
        """Retrieves an element, potentially returning a copy.

        Args:
            name (str): The name of the element.

        Returns:
            object | None: The element (or a copy) if found, otherwise None.
        """
        ...

    def get_new(self, name: str) -> object | None:
        """Retrieves an element or a copy of it.

        Args:
            name (str): The name of the element.

        Returns:
            object | None: The element or a copy if it exists, otherwise None.
        """
        element = self.elements.get(name)
        return element.__copy__() if element else None

    @staticmethod
    def get_load_data():
        return Loader.global_load_data
