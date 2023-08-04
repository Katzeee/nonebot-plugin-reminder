import re
import datetime


pattern = r"\d+[smhdw]"


def parse_time(time_str: str):  # -> datetime.timedelta:
    matches = re.findall(pattern, time_str)
    delta = datetime.timedelta(0)
    for match in matches:
        unit = match[-1]
        num = match[0:-1]
        if unit == "s":
            delta += datetime.timedelta(seconds=int(num))
        elif unit == "m":
            delta += datetime.timedelta(minutes=int(num))
        elif unit == "h":
            delta += datetime.timedelta(hours=int(num))
        elif unit == "d":
            delta += datetime.timedelta(days=int(num))
        elif unit == "w":
            delta += datetime.timedelta(weeks=int(num))
        else:
            raise ValueError(f"no unit named {unit}")
    return delta
