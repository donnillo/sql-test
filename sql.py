from datetime import date, time
from contextlib import contextmanager

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from tabulate import tabulate

import model.employees
from model.employees import EmployeePresence


from typing import Protocol, ClassVar
from typing import Generator
from utils.fake import yesterday
from utils.fake.employees import get_presence, get_employee


class TaskMixin(Protocol):
    Base: ClassVar[type[DeclarativeBase]]

    def generate_data(self) -> list[type[DeclarativeBase]]:
        ...


class Database(TaskMixin, Protocol):
    engine: sqlalchemy.engine.Engine
    Session: sessionmaker

    def __init__(self):
        self.engine = create_engine("duckdb:///:memory:")
        self.Session = sessionmaker(self.engine)
        self.Base.metadata.create_all(self.engine)
        self.populate()

    @property
    @contextmanager
    def orm(self) -> Generator[sqlalchemy.orm.Session, None, None]:
        yield self.Session()

    def populate(self):
        with self.orm as session:
            data = self.generate_data()
            session.add_all(data)
            session.commit()

    def print_table(self):
        ...


class TaskOne(TaskMixin):
    Base = model.employees.Base

    def generate_data(self):
        return [
            EmployeePresence(
                employee=employee,
                day=yesterday,
                presence=get_presence(),
            ) for employee in get_employee()
        ]


class TaskOneDatabase(TaskOne, Database):
    def print_table(self):
        with self.orm as session:
            result = session.execute(
                select(*EmployeePresence.__table__.columns)
            ).all()

        headers = result[0]._fields
        print(tabulate(result, headers=headers, tablefmt="rounded_outline"))


if __name__ == "__main__":
    db = TaskOneDatabase()
    db.print_table()
