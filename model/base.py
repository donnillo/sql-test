from __future__ import annotations

import enum

from sqlalchemy import Sequence
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import has_inherited_table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from utils.string import camel_to_snake


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls):
        if not has_inherited_table(cls):  # type: ignore
            return camel_to_snake(cls.__name__)


class PersonType(enum.StrEnum):
    employee = enum.auto()
    client = enum.auto()


person_id = Sequence("person_id_seq")


class Person(Base):
    id: Mapped[int] = mapped_column(
        Integer, person_id, primary_key=True,
        server_default=person_id.next_value()
    )
    name: Mapped[str]
    type: Mapped[PersonType]

    __mapper_args__ = dict(polymorphic_on="type")

    def __init__(self, name):
        self.name = name
