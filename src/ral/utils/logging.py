from __future__ import annotations
import logging


class CustomLogging:

    @classmethod
    def create_config(cls) -> dict:
        config = {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] [%(levelname)s] [%(name)s]"
                    + " %(message)s",
                    "datefmt": r"%Y-%m-%d %H:%M:%S",
                },
                "colored": {
                    "()": ColorFormmater,
                    "format": "[%(asctime)s] [%(levelname)s] [%(name)s]"
                    + " %(message)s",
                    "datefmt": r"%Y-%m-%d %H:%M:%S",
                },
                "detail": {
                    "format": "[%(asctime)s] [%(levelname)s] [%(name)s]"
                    + " [%(filename)s:%(lineno)d] %(message)s",
                    "datefmt": r"%Y-%m-%d %H:%M:%S.%f",
                },
                "colored-detail": {
                    "()": ColorFormmater,
                    "format": "[%(asctime)s] [%(levelname)s] [%(name)s]"
                    + " %(message)s",
                    "datefmt": r"%Y-%m-%d %H:%M:%S.%f",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "colored",
                    "level": "DEBUG",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "formatter": "detail",
                    "level": None,
                    "filename": "app.log",
                },
            },
            "loggers": {
                "root": {
                    "handlers": ["console", "file"],
                    "level": "DEBUG",
                    "propagate": False,
                },
                "uvicorn": {
                    "handlers": ["console"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
        return config


class ColorFormmater(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._colors = {
            "DEBUG": "\033[94m",  # Light blue text
            "INFO": "\033[92m",  # Green text
            "WARNING": "\033[93m",  # Yellow text
            "ERROR": "\033[91m",  # Red text
            "CRITICAL": "\033[91m",  # Red text
            "DEFAULT": "\033[0m",  # Reset to default
        }

    def format(self, record):
        original_level = record.levelname
        record.levelname = (
            f"{self._colors[original_level]}"
            + f"{original_level}{self._colors['DEFAULT']}"
        )
        msg = super().format(record)
        record.levelname = original_level  # restore original levelname
        return msg
