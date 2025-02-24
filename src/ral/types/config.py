from typing import TypedDict


class ConfigJson(TypedDict):
    """TypedDict for the JSON configuration file."""

    host: str
    port: int
