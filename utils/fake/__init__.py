import datetime

yesterday = datetime.datetime.now().date() - datetime.timedelta(1)


def last_n_weeks(n):
    for day in [
        yesterday - datetime.timedelta(days)
        for days in range(7 * n - 1, -1, -1)
    ]:
        yield day
