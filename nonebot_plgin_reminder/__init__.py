from nonebot import get_driver
from nonebot import require
require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

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

async def ohayo():
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=742827356, message=f"ohayo")


async def oyasumi():
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=742827356, message=f"oyasumi")

scheduler.add_job(test_func, "cron", hour=14, minute=25, id="test timer")
scheduler.add_job(ohayo, "cron", hour=7, minute=30)
scheduler.add_job(oyasumi, "cron", hour=18, minute=35)
#scheduler.add_job(ohayo, "interval", hour=1, minute=30)


