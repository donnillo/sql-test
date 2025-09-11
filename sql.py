import sys

from tasks.first import TaskOneDatabase
from tasks.second import TaskTwoDatabase


if __name__ == "__main__":
    task = int(sys.argv[1])
    if task == 1:
        db = TaskOneDatabase()
    elif task == 2:
        db = TaskTwoDatabase()
    db.print_table()
