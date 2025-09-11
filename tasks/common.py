from contextlib import contextmanager
from typing import Protocol
from typing import Generator

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedClassProtocol
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate


class TaskMixin(Protocol):
    Base: type[DeclarativeBase]
    target: MappedClassProtocol

    def generate_data(self) -> list[MappedClassProtocol]:
        ...


class Database(TaskMixin, Protocol):
    engine: sqlalchemy.engine.Engine
    Session: sessionmaker

    def __init__(self):
        self.engine = create_engine("duckdb:///:memory:")
        self.Session = sessionmaker(self.engine)
        self.Base.metadata.create_all(self.engine)
        self.populate()

    @contextmanager
    def orm(self) -> Generator[sqlalchemy.orm.Session, None, None]:
        yield self.Session()

    def populate(self):
        with self.orm() as session:
            data = self.generate_data()
            session.add_all(data)
            session.commit()

    def print_table(self, max_rows: int = 20):
        with self.orm() as session:
            rows = session.execute(
                select(*self.target.__table__.columns)
            ).all()

        headers = rows[0]._fields
        if (skipped := abs(min(max_rows - len(rows), 0))) > 1:
            rows = [
                *rows[:max_rows // 2],
                tuple(None for _ in headers),
                *rows[max_rows // 2 + skipped + 1:]
            ]

        table = tabulate(
            rows,
            headers=headers,
            tablefmt="rounded_outline",
            missingval="\u00b7" * 3,
            floatfmt=",.2f",
        )

        width = len(table.partition("\n")[0])
        if (title := getattr(self.target.__table__, "name", None)):
            print(f"{f" {title} ":\u2500^{width}}")
        print(table)
        if skipped > 1:
            print(f"{skipped} rows skipped")
