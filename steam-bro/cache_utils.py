from pathlib import Path
from pathlib import Path
from typing import List, Optional

import pandas as pd


_CACHE_DIR = Path(__file__).parent / "cache"


def _ensure_cache_dir() -> Path:
    """Make sure the cache directory exists and return its path."""
    _CACHE_DIR.mkdir(exist_ok=True)
    return _CACHE_DIR


def get_cache_key(file_name: str) -> str:
    """
    Return the logical cache key for a chat.
    Right now it's just the file name, but this indirection
    lets us switch to IDs or hashes later without touching callers.
    """
    return file_name


def get_cache_path(key: str) -> Path:
    """Get the on-disk path for a given cache key."""
    cache_dir = _ensure_cache_dir()
    return cache_dir / f"{key}.pkl"


def save_chat_df(file_name: str, df: pd.DataFrame) -> Path:
    """
    Save a chat DataFrame to the cache and return the path.
    """
    key = get_cache_key(file_name)
    path = get_cache_path(key)
    df.to_pickle(path)
    return path


def load_chat_df(file_name: str) -> Optional[pd.DataFrame]:
    """
    Load a cached chat DataFrame by file name.
    Returns None if it does not exist.
    """
    key = get_cache_key(file_name)
    path = get_cache_path(key)
    if not path.is_file():
        return None
    return pd.read_pickle(path)


def list_cached_chats() -> List[str]:
    """
    List all cached chats by their logical keys (currently file names).
    """
    cache_dir = _ensure_cache_dir()
    return [
        p.stem  # strip ".pkl"
        for p in sorted(cache_dir.glob("*.pkl"))
    ]


def delete_chat(file_name: str) -> None:
    """
    Remove a chat from the cache. Does nothing if it doesn't exist.
    """
    key = get_cache_key(file_name)
    path = get_cache_path(key)
    if path.is_file():
        path.unlink()
