import json
import os
import sys
from csv import DictReader
from datetime import date, timedelta

import requests
from sentry_sdk import capture_exception

PATTERN_CSV_FILE_NAME = "epex_trades_{date}.csv"
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
TRADE_URL = f"{BASE_URL}/trades"
CSV_DIR = os.getenv("CSV_DIR", os.getcwd())


def get_existing_trade_ids(delivery_day: date) -> list[str]:
    response = requests.get(TRADE_URL, params={"delivery_day": delivery_day.isoformat()}, timeout=30)
    trades = response.json()
    return [trade["id"] for trade in trades]


def add_new_trades(existing_trade_ids: list[str], delivery_day: date):
    csv_filename = PATTERN_CSV_FILE_NAME.format(date=delivery_day.strftime("%Y%m%d"))
    csv_path = os.path.join(CSV_DIR, csv_filename)
    count = 0
    try:
        with open(csv_path) as csvfile:
            trade_reader = DictReader(csvfile)

            for trade in trade_reader:
                if trade["id"] in existing_trade_ids:
                    continue
                response = requests.post(TRADE_URL, json=trade, timeout=30)
                if response.status_code != 200:
                    print(f"Request failed with status {response.status_code} and message:")
                    print(json.dumps(response.json(), indent=2))
                    exit(1)

                count += 1
    except FileNotFoundError:
        print(f"File {csv_filename} not found at {CSV_DIR}", file=sys.stderr)
        exit(1)

    print(f"{count} new trades added.")


def main():
    yesterday = date.today() - timedelta(days=1)
    existing_trade_ids = get_existing_trade_ids(yesterday)
    add_new_trades(existing_trade_ids, yesterday)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        capture_exception(e)
        raise
