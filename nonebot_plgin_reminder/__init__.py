from nonebot import get_driver
from nonebot.log import logger
from nonebot import require
try:
    scheduler = require("nonebot_plugin_apscheduler").scheduler
except Exception:
    scheduler = None
import nonebot
import io
from .config import Config
from nonebot import on_command
from .__utils__ import parse_interval, parse_cron, JOBS_FILE
import json
from nonebot.adapters.console import MessageEvent
from nonebot.adapters import Message
from nonebot.params import CommandArg


global_config = get_driver().config
config = Config.parse_obj(global_config)

timer = on_command("timer")
listall = on_command("list")


@timer.handle()
async def handle_function(event: MessageEvent, args: Message = CommandArg()):
    bot = nonebot.get_bot()
    if location := args.extract_plain_text():
        await timer.finish(f"今天{location}的天气是...")


async def test_func():
    bot = nonebot.get_bot()
    await bot.send_private_msg(user_id=326578901, message=f"timer")


@listall.handle()
async def _():
    my_io = io.StringIO()
    scheduler.print_jobs(out=my_io)
    await listall.finish(my_io.getvalue())

if scheduler:
    logger.info("Start parsing jobs..")
    with open(JOBS_FILE) as f:
        jobs_json = json.load(f)
    for key, value in jobs_json.items():
        if value["type"] == "cron":
            parse_cron(value)
        elif value["type"] == "interval":
            parse_interval(value)
