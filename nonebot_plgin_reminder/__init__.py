import json
import datetime
import nonebot
import io
from nonebot.log import logger
from nonebot import on_command
from nonebot.adapters import Message, Event
from nonebot.params import CommandArg
from .utils import parse_time
from .config import config, SCHEDULER
from .addjob import *


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
    for job in jobs_json:
        if job["type"] == "cron":
            deserialize_cron(job)
        elif job["type"] == "interval":
            deserialize_interval(job)
        elif job["type"] == "date":
            deserialize_date(job)
    my_io = io.StringIO()
    SCHEDULER.print_jobs(out=my_io)
