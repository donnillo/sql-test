from utils.args import get_database_from_args


if __name__ == "__main__":
    db = get_database_from_args()
    db.print_table()
    db.run_query()
