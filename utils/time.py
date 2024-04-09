import json
from datetime import datetime

TIME_DB = None


def load_time_db(path: str = "../db/time_capability.json") -> dict:
    global TIME_DB

    if not TIME_DB:
        with open(path, 'r') as db_file:
            TIME_DB = json.loads(db_file.read())
    return TIME_DB


def get_time_capability(employee_id: str | int) -> dict:
    time_db = load_time_db()
    records = [record for record in time_db["records"]]
    for record in records:
        if record["employee_id"] == employee_id:
            return record


def get_current_datetime(format: str = "%A, %d %B %Y %I:%M %p") -> str:
    current_datetime = datetime.now()
    return current_datetime.strftime(format)
