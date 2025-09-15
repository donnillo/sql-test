import argparse

from tasks.common import Database


def get_database_from_args() -> Database:
    parser = argparse.ArgumentParser(prog="sql-test")
    parser.add_argument(
        "--task", "-t", choices=(1, 2), type=int,
        help="specify task number"
    )
    args = parser.parse_args()
    match args.task:
        case 1:
            from tasks.first import TaskOneDatabase as Database
        case 2:
            from tasks.second import TaskTwoDatabase as Database
    return Database()
