import os
from functools import cache
from typing import Optional
from pathlib import Path


@cache
def get_data_directory() -> Path:
    """_summary_

    Raises:
        RuntimeError: _description_

    Returns:
        _description_
    """
    data_directory_path: Optional[str] = os.getenv("DS_DATA", None)
    if data_directory_path:
        return Path(data_directory_path)
    data_directory = Path.cwd() / "data"
    return data_directory


def data_catalog_exists() -> bool:
    return False
