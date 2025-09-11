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
    pass
