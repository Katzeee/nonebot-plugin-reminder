import nonebot
import json
import datetime
from nonebot.adapters import Event
from .config import config, SCHEDULER

datetime_format = '%Y-%m-%d %H:%M:%S'


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


async def job_send(content: str, event: Event):
    bot = nonebot.get_bot()
    try:
        await bot.send(event, message=eval(f'f"""{content}"""'))
    except Exception as e:
        await bot.send(event, message=repr(e))


# https://blog.csdn.net/kobepaul123/article/details/123616575


def deserialize_cron(job_desc: dict):
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
    args = job_desc.get("args", [])
    group_id = job_desc.get("group_id")
    user_id = job_desc.get("user_id")
    if group_id and user_id:
        return
    elif group_id:
        args.append(group_id)
        SCHEDULER.add_job(
            job_group_send,
            "cron",
            year=year,
            month=month,
            day=day,
            week=week,
            day_of_week=day_of_week,
            hour=hour,
            minute=minute,
            second=second,
            start_date=start_date,
            end_date=end_date,
            jitter=jitter,
            args=args,
        )
    elif user_id:
        args.append(user_id)
        SCHEDULER.add_job(
            job_private_send,
            "cron",
            year=year,
            month=month,
            day=day,
            week=week,
            day_of_week=day_of_week,
            hour=hour,
            minute=minute,
            second=second,
            start_date=start_date,
            end_date=end_date,
            jitter=jitter,
            args=args,
        )
    else:
        return


def deserialize_interval(job_desc: dict):
    weeks = job_desc.get("weeks") or 0
    days = job_desc.get("days") or 0
    hours = job_desc.get("hours") or 0
    minutes = job_desc.get("minutes") or 0
    seconds = job_desc.get("seconds") or 0
    start_date = job_desc.get("start_date")
    end_date = job_desc.get("end_date")
    jitter = job_desc.get("jitter")
    args = job_desc.get("args", [])
    group_id = job_desc.get("group_id")
    user_id = job_desc.get("user_id")
    if group_id and user_id:
        return
    elif group_id:
        args.append(group_id)
        SCHEDULER.add_job(
            job_group_send,
            "interval",
            weeks=weeks,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            start_date=start_date,
            end_date=end_date,
            jitter=jitter,
            args=args,
        )
    elif user_id:
        args.append(user_id)
        SCHEDULER.add_job(
            job_private_send,
            "interval",
            weeks=weeks,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            start_date=start_date,
            end_date=end_date,
            jitter=jitter,
            args=args,
        )
    else:
        return

def deserialize_date(job_desc: dict):
    date = datetime.datetime.strptime(job_desc.get("date"), datetime_format)
    args = job_desc.get("args", [])
    group_id = job_desc.get("group_id")
    user_id = job_desc.get("user_id")
    if group_id and user_id:
        return
    elif group_id:
        args.append(group_id)
        SCHEDULER.add_job(
            job_group_send,
            "date",
            run_date=date,
            args=args,
        )
    elif user_id:
        args.append(user_id)
        SCHEDULER.add_job(
            job_private_send,
            "date",
            run_date=date,
            args=args,
        )
    else:
        return



def serialize_jobs():
    jobs = SCHEDULER.get_jobs()
    jobs_list = []
    for job in jobs:
        job_dict = {}
        if job.func.__name__ == 'job_group_send':
            job_dict['group_id'] = str(job.args[1])
        elif job.func.__name__ == 'job_private_send':
            job_dict['user_id'] = str(job.args[1])
        if job.trigger.__class__.__name__ == 'CronTrigger':
            job_dict['type'] = 'cron' 
            for f in job.trigger.fields:
                if not f.is_default:
                    job_dict[f.name] = str(f)
        elif job.trigger.__class__.__name__ == 'DateTrigger':
            job_dict['type'] = 'date'
            job_dict['date'] = job.trigger.run_date.strftime(datetime_format)
        else:
            print(job.trigger.__class__.__name__)
            job_dict['type'] = 'interval'
        job_dict['args'] = [job.args[0]]
        jobs_list.append(job_dict)
    with open(config.JOBS_FILE_PATH, 'w') as f:
        json.dump(jobs_list, f, ensure_ascii=False, indent=2)


def add_timer(run_date, args):
    event = args[1]
    if event.message_type == 'private':
        args[1] = event.user_id
        SCHEDULER.add_job(job_private_send, "date", run_date=run_date, args=args)
    elif event.message_type == 'group':
        args[1] = event.group_id
        SCHEDULER.add_job(job_group_send, "date", run_date=run_date, args=args)
    serialize_jobs()
