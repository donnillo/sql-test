from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import aliased

import model.employees
from model.employees import EmployeePresence
from tasks.common import Database, TaskMixin
from utils.dates import yesterday
from utils.fake.employees import get_employee, get_presence


class TaskOne(TaskMixin):
    Base = model.employees.Base
    target = EmployeePresence

    def generate_data(self):
        return [
            EmployeePresence(
                employee=employee,
                day=yesterday,
                presence=get_presence(),
            ) for employee in get_employee()
        ]


class TaskOneDatabase(TaskOne, Database):
    def generate_query(self):
        hours = select(
            func.generate_series(0, 23)
            .table_valued("hour").render_derived("hours")
        ).subquery("hours")

        arrival = aliased(EmployeePresence, name="arrival")
        departure = aliased(EmployeePresence, name="departure")

        hourly = select(
            hours.c.hour,
            (
                func.count(arrival.employee_id.distinct()) -
                func.count(departure.employee_id.distinct())
            ).label("count"),
        ).join(
            arrival,
            hours.c.hour == func.extract("hour", arrival.arrival),
            isouter=True,
        ).join(
            departure,
            hours.c.hour == func.extract("hour", departure.departure),
            isouter=True,
        ).group_by(
            hours.c.hour,
        ).order_by(
            hours.c.hour.asc(),
        ).subquery("hourly")

        return select(
            hourly.c.hour,
            func.coalesce(
                func.sum(
                    hourly.c.count
                ).over(
                    order_by=hourly.c.hour,
                    rows=(None, -1),
                ), 0
            ).label("num_persons")
        )
