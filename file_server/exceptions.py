from typing import final

@final
class FileNotFoundError(Exception):
    """Исключение возникает при отсутствии загружаемого файла."""
