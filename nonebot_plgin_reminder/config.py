from pydantic import BaseModel, Extra
from pathlib import Path
from nonebot import require


try:
    SCHEDULER = require("nonebot_plugin_apscheduler").scheduler
except Exception:
    SCHEDULER = None


class Config(BaseModel, extra=Extra.ignore):
    JOBS_FILE_PATH = Path().cwd() / "data" / "jobs.json"


config = Config()
