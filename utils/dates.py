import datetime

yesterday = datetime.datetime.now().date() - datetime.timedelta(1)


def last_n_weeks(n):
    for day in [
        yesterday - datetime.timedelta(days)
        for days in range(7 * n - 1, -1, -1)
    ]:
        yield day


def last_n_months(n):
    y, m, d, *_ = yesterday.timetuple()
    y -= n // 12
    m -= n % 12
    try:
        day = datetime.date(y, m, d)
    except ValueError:
        day = datetime.date(y, m % 12 + 1, 1) - datetime.timedelta(1)
    while day <= yesterday:
        yield day
        day += datetime.timedelta(1)
