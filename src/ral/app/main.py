import platform
from contextlib import asynccontextmanager
from logging import getLogger
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from ral.utils.logging import CustomLogging
from ral.io import ConfigReader

config = ConfigReader.read_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.logger = getLogger()
    yield


app = FastAPI(root_path="/fastapi", lifespan=lifespan)


@app.get("/os/")
async def get_os() -> str:
    os = platform.system()
    return os


def start():
    uvicorn.run(
        "ral.app.main:app",
        host=config.host,
        port=config.port,
        log_config=CustomLogging.create_config(),
    )


def dev():
    filepath = Path(__file__)
    for path in list(filepath.parents):
        if path.name == "src":
            src_dirpath = path
            break
    uvicorn.run(
        "ral.app.main:app",
        reload=True,
        reload_dirs=[src_dirpath],
        host=config.host,
        port=config.port,
        log_config=CustomLogging.create_config(),
    )
