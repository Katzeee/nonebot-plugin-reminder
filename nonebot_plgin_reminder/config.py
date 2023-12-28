from pydantic import BaseModel, Extra
from pathlib import Path
from nonebot import require
from nonebot import get_driver


try:
    SCHEDULER = require("nonebot_plugin_apscheduler").scheduler
except Exception:
    logger.error("Please install nonebot_plugin_apscheduler")
    SCHEDULER = None


class Config(BaseModel, extra=Extra.ignore):
    JOBS_FILE_PATH = Path().cwd() / "data" / "jobs.json"

global_config = get_driver().config
config = Config.parse_obj(global_config)
