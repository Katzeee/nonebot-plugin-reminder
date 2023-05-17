from pathlib import Path
import nonebot
from nonebot import require

try:
    scheduler = require("nonebot_plugin_apscheduler").scheduler
except Exception:
    scheduler = None

JOBS_FILE = Path() / "data" / "jobs.json"


async def job_group_send(content: str, group_id):
    bot = nonebot.get_bot()
    try:
        await bot.send_group_msg(group_id=group_id, message=eval(f'f"""{content}"""'))
    except Exception as e:
        await bot.send_group_msg(group_id=group_id, message=repr(e))

async def job_private_send(content: str, user_id):
    bot = nonebot.get_bot()
    try:
        await bot.send_private_msg(user_id=user_id, message=eval(f'f"""{content}"""'))
    except Exception as e:
        await bot.send_private_msg(user_id=user_id, message=repr(e))



# https://blog.csdn.net/kobepaul123/article/details/123616575

def parse_cron(job_desc: dict):
    year = job_desc.get("year")
    month = job_desc.get("month")
    day = job_desc.get("day")
    week = job_desc.get("week")
    day_of_week = job_desc.get("day_of_week")
    hour = job_desc.get("hour")
    minute = job_desc.get("minute")
    second = job_desc.get("second")
    start_date = job_desc.get("start_date")
    end_date = job_desc.get("end_date")
    jitter = job_desc.get("jitter")
    args = job_desc.get("args")
    group_id = job_desc.get("group_id")
    user_id = job_desc.get("user_id")
    if group_id and user_id:
        return
    elif group_id:
        args.append(group_id)
        scheduler.add_job(job_group_send, "cron", year=year, month=month, day=day, week=week, day_of_week=day_of_week, hour=hour,
                      minute=minute, second=second, start_date=start_date, end_date=end_date, jitter=jitter, args=args)
    elif user_id:
        args.append(user_id)
        scheduler.add_job(job_private_send, "cron", year=year, month=month, day=day, week=week, day_of_week=day_of_week, hour=hour,
                      minute=minute, second=second, start_date=start_date, end_date=end_date, jitter=jitter, args=args)
    else:
        return



def parse_interval(job_desc: dict):
    weeks = job_desc.get("weeks") or 0
    days = job_desc.get("days") or 0
    hours = job_desc.get("hours") or 0
    minutes = job_desc.get("minutes") or 0
    seconds = job_desc.get("seconds") or 0
    start_date = job_desc.get("start_date")
    end_date = job_desc.get("end_date")
    jitter = job_desc.get("jitter")
    args = job_desc.get("args")
    group_id = job_desc.get("group_id")
    user_id = job_desc.get("user_id")
    if group_id and user_id:
        return
    elif group_id:
        args.append(group_id)
        scheduler.add_job(job_group_send, "interval", weeks=weeks, days=days, hours=hours, minutes=minutes,
                      seconds=seconds, start_date=start_date, end_date=end_date, jitter=jitter, args=args)
    elif user_id:
        args.append(user_id)
        scheduler.add_job(job_private_send, "interval", weeks=weeks, days=days, hours=hours, minutes=minutes,
                      seconds=seconds, start_date=start_date, end_date=end_date, jitter=jitter, args=args)
    else:
        return
