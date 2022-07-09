"""s2b client entrypoint"""

import os

from celery.result import AsyncResult
from fastapi import Body, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from iotcommon.logging import ServiceName, init_logging
from iotcommon.worker import create_task

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = f"{CUR_PATH.split('/main.py')[0]}/static"
TEMPLATE_PATH = f"{CUR_PATH.split('/main.py')[0]}/templates"

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
templates = Jinja2Templates(directory=TEMPLATE_PATH)
logger = init_logging(ServiceName.S2B)


@app.get("/")
def home(request: Request):
    logger.debug("home.GET")
    return templates.TemplateResponse("home.html", context={"request": request})


@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    logger.debug("tasks.POST")
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):
    logger.debug("tasks.GET")
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
