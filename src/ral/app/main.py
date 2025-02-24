import platform
import shutil
import subprocess
from contextlib import asynccontextmanager
from logging import getLogger
from pathlib import Path
from typing import Literal

import psutil
import uvicorn
from fastapi import FastAPI
from fastapi import Query
from fastapi.responses import JSONResponse

from ral.io import ConfigReader
from ral.utils.logging import CustomLogging

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


@app.get("/disk-usage/")
async def get_disk_usage(
    unit: Literal["KB", "MB", "GB"] = Query()
) -> JSONResponse:
    match unit:
        case "KB":
            unit_val = 1024
        case "MB":
            unit_val = 1024**2
        case "GB":
            unit_val = 1024**3
    disk_usage = shutil.disk_usage("/")
    return JSONResponse(
        {
            "total": disk_usage.total / unit_val,
            "used": disk_usage.used / unit_val,
            "free": disk_usage.free / unit_val,
        }
    )


@app.post("/run-command/")
async def run_command(
    command: str,
    cwd: str = Query(
        default=".",
        description="Working directory where the command will be executed.",
    ),
):
    process = subprocess.Popen(
        command,
        shell=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    pid = process.pid
    response = JSONResponse(content={"pid": pid})
    return response


@app.post("/kill-process/")
async def kill_process(pid: int = Query(..., description="Process ID")):
    try:
        if psutil.pid_exists(pid):
            process = psutil.Process(pid)
            process.kill()
            responce = JSONResponse(
                content={"message": f"Succesfully killed process {pid}."}
            )
        else:
            responce = JSONResponse(
                content={"message": f"Process {pid} does not exist."}
            )
        return responce
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


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
