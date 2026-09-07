import datetime
from config import LOG_FILE
import os

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def log_event(event: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {event}\n")