import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from model.base import Base, Person


class Client(Person):
    __mapper_args__ = dict(polymorphic_identity="client")


class ClientBalance(Base):
    client_id: Mapped[int] = mapped_column(
        ForeignKey(Client.id), primary_key=True
    )
    client: Mapped[Client] = relationship(lazy="joined", innerjoin=True)
    day: Mapped[datetime.date] = mapped_column(primary_key=True)
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=13, scale=2)  # max: 99_999_999_999.99
    )

    def __repr__(self):
        return f"{self.client.name:^15} {self.day!s} {self.balance!s}"
