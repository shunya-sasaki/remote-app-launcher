from __future__ import annotations
from dataclasses import dataclass
from ral.types import ConfigJson


@dataclass
class Config:
    host: str = "0.0.0.0"
    port: int = 8000

    @classmethod
    def from_json(cls, data: dict) -> Config:
        config = Config(host=data["host"], port=data["port"])
        return config

    def to_json(self) -> ConfigJson:
        config = ConfigJson(host=self.host, port=self.port)
        return config
