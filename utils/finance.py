import json

FINANCE_DB = None


def load_finance_db(path: str = "../db/financial_capability.json") -> dict:
    global FINANCE_DB

    if not FINANCE_DB:
        with open(path, 'r') as db_file:
            FINANCE_DB = json.loads(db_file.read())
    return FINANCE_DB


def get_finance_capability(employee_id: str | int) -> dict:
    finance_db = load_finance_db()
    records = [record for record in finance_db["records"]]
    for record in records:
        if record["employee_id"] == employee_id:
            return record
