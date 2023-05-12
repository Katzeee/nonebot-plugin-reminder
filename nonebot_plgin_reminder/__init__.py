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
global_config = get_driver().config
config = Config.parse_obj(global_config)

remindme = on_command("remindme")
listall = on_command("list")


@remindme.handle()
async def handle_function():
    bot = nonebot.get_bot()
    await bot.send_private_msg(user_id=326578901, message=f"remind")
    await remindme.finish("ti xing")


async def test_func():
    bot = nonebot.get_bot()
    await bot.send_private_msg(user_id=326578901, message=f"timer")


@listall.handle()
async def _():
    my_io = io.StringIO()
    scheduler.print_jobs(out=my_io)
    await listall.finish(my_io.getvalue())
