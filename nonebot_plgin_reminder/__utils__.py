from pathlib import Path
import nonebot

try:
    scheduler = require("nonebot_plugin_apscheduler").scheduler
except Exception:
    scheduler = None

JOBS_FILE = Path() / "data" / "jobs.json"

def job_printf(content:str):
    bot = nonebot.get_bot()
    bot.send_group_msg(group_id=742827356, message=eval(f'f"""{content}"""'))

def parse_interval(job_desc: dict):
    weeks = job_desc.get("weeks") or 0
    days = job_desc.get("days") or 0
    hours = job_desc.get("hours") or 0
    minutes = job_desc.get("minutes") or 0
    seconds = job_desc.get("seconds") or 0
    start_date = job_desc.get("start_date")
    end_date = job_desc.get("end_date")
    args = job_desc.get("args")
    scheduler.add_job(job_printf, "interval", weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds, start_date=start_date, end_date=end_date, args=args)

