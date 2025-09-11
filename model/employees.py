from __future__ import annotations

import datetime
from dataclasses import dataclass

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import attribute_keyed_dict
from sqlalchemy.orm import composite

from model.base import Base, Person


@dataclass(slots=True, repr=False)
class Presence:
    arrival: datetime.time
    departure: datetime.time

    def __repr__(self):
        return f"{self.arrival:%H:%M}\N{en dash}{self.departure:%H:%M}"


class Employee(Person):
    on_day: Mapped[dict[datetime.date, EmployeePresence]] = relationship(
        collection_class=attribute_keyed_dict("day"),
        back_populates="employee",
    )

    __mapper_args__ = dict(polymorphic_identity="employee")


class EmployeePresence(Base):
    employee_id: Mapped[int] = mapped_column(
        ForeignKey(Employee.id), primary_key=True
    )
    employee: Mapped[Employee] = relationship(lazy="joined", innerjoin=True)
    day: Mapped[datetime.date] = mapped_column(primary_key=True)
    presence: Mapped[Presence] = composite(
        mapped_column("arrival"),
        mapped_column("departure"),
    )

    def __repr__(self):
        return f"{self.employee.name:^15} {self.day!s} {self.presence!s}"
