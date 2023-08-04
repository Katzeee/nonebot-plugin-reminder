from nonebot import get_driver
from nonebot.log import logger
from .config import Config, SCHEDULER
from nonebot import on_command
from .addjob import parse_interval, parse_cron, add_timer
from nonebot.adapters import Message, Event
from nonebot.params import CommandArg
import json
import nonebot
import io

global_config = get_driver().config
config = Config.parse_obj(global_config)
logger.debug(config)

timer = on_command("timer")
listall = on_command("list")


@timer.handle()
async def _(event: Event, args: Message = CommandArg()):
    bot = nonebot.get_bot()
    logger.info(nonebot.get_bots())
    if arg_str := args.extract_plain_text():
        arg_list = arg_str.split(" ")
        minutes = arg_list[-1]
        if len(arg_list) < 2 or not minutes.isdigit():
            await timer.finish(
                "========\nusage: /timer remind me 10\n========\nwhich means remind you after 50 minutes"
            )
        arg_list.pop()
        content = " ".join(arg_list)
        arg_list = [content, event]
        logger.info(minutes)
        logger.info(arg_list)
        add_timer(minutes, arg_list)
        await timer.finish(f'I will remind you "{arg_list[0]}" in {minutes} minutes!')


async def test_func():
    bot = nonebot.get_bot()
    await bot.send_private_msg(user_id=326578901, message="timer")


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
    # bot.send_private_msg()
