import json
import datetime
import nonebot
import io
from nonebot import get_driver
from nonebot.log import logger
from nonebot import on_command
from nonebot.adapters import Message, Event
from nonebot.params import CommandArg
from .utils import parse_time
from .config import Config, SCHEDULER
from .addjob import parse_interval, parse_cron, add_timer

global_config = get_driver().config
config = Config.parse_obj(global_config)
bot = nonebot.get_bot()

timer = on_command("timer")
listall = on_command("list")


@timer.handle()
async def _(event: Event, args: Message = CommandArg()):
    logger.info(nonebot.get_bots())
    if arg_str := args.extract_plain_text():
        arg_list = arg_str.split(" ")
        time_str = arg_list[-1]
        if len(arg_list) < 2:
            await timer.finish(
                """
==========================
usage: /timer remind me 10
==========================
which means remind you after 50 minutes
"""
            )
        arg_list.pop()
        content = " ".join(arg_list)
        arg_list = [content, event]

        now = datetime.datetime.now()
        delta = parse_time(time_str)
        run_date = now + delta
        add_timer(run_date, arg_list)
        await timer.finish(
            f'I\'ll remind you "{arg_list[0]}" in {time_str} at {run_date.strftime("%Y-%m-%d %H:%M:%S")}!'
        )


@listall.handle()
async def _():
    my_io = io.StringIO()
    SCHEDULER.print_jobs(out=my_io)
    await listall.finish(my_io.getvalue())


if SCHEDULER:
    logger.info("Start parsing jobs..")
    with open(config.JOBS_FILE_PATH) as f:
        jobs_json = json.load(f)
    for key, value in jobs_json.items():
        if value["type"] == "cron":
            parse_cron(value)
        elif value["type"] == "interval":
            parse_interval(value)
    my_io = io.StringIO()
    SCHEDULER.print_jobs(out=my_io)
