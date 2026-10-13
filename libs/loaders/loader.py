from pathlib import Path


class Loader:
    """Base class for loaders.

    Provides basic functionality for loading, storing, and retrieving elements.
    """
    elements: dict[str, object]

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
        for iPath in path.iterdir():
            self.load(iPath)

    def add(self, element: object, name: str) -> None:
        """Adds an element to the storage.

        Args:
            element (object): The element to add.
            name (str): The name associated with the element.
        """
        self.elements[name] = element

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
