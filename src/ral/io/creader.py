import json
from pathlib import Path

from ral.models import Config


class ConfigReader:

    @classmethod
    def read_config(cls, config_file: str = "config.json") -> Config:
        config_filepath = Path(config_file)
        if config_filepath.exists():
            with open(config_filepath, "r") as file:
                config_json = json.load(file)
                return Config.from_json(config_json)
        else:
            return Config()
