import sys
from argparse import ArgumentParser
from datetime import date

from sentry_sdk import capture_exception
from tabulate import tabulate
from tortoise import Tortoise, run_async

from power.generate_report import generate_trade_report
from power.settings import DB_MODULES, settings


def parse_args(args):
    parser = ArgumentParser()
    parser.add_argument("-t", "--trader_id", type=str, required=True)
    parser.add_argument("-d", "--delivery_day", type=lambda d: date.fromisoformat(d), required=False)
    return parser.parse_args(args)


def print_report(report: list[dict]):
    if not report:
        print("No trades found.")
    print(tabulate(report, headers="keys"))


async def main():
    try:
        args = parse_args(sys.argv[1:])
        await Tortoise.init(db_url=settings.DB_URL, modules=DB_MODULES)
        report = await generate_trade_report(args.trader_id, args.delivery_day)
        print_report(report["records"])
    except Exception as e:
        capture_exception(e)
        raise


if __name__ == "__main__":
    run_async(main())
