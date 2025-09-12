from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import case

import model.clients
from model.clients import ClientBalance
from tasks.common import Database, TaskMixin
from utils.dates import last_n_months
from utils.fake.clients import get_clients, get_balance


class TaskTwo(TaskMixin):
    Base = model.clients.Base
    target = ClientBalance

    def generate_data(self):
        # clients = [*get_clients()]
        clients = [next(get_clients())]  # get only one client for simple test
        balances = [get_balance() for _ in clients]
        return [
            ClientBalance(
                client=client,
                day=day,
                balance=next(balance),
            ) for day in last_n_months(1)
            for client, balance in zip(clients, balances)
        ]


class TaskTwoDatabase(TaskTwo, Database):
    def generate_query(self):
        pre_periodized = select(
            ClientBalance.client_id,
            ClientBalance.day,
            ClientBalance.balance,
            func.sum(
                case(
                    (ClientBalance.balance == 0, 1),
                    else_=0,
                )
            ).over(
                order_by=(ClientBalance.client_id, ClientBalance.day)
            ).label("period"),
            func.lead(
                ClientBalance.balance, 1,
            ).over(
                order_by=(ClientBalance.client_id, ClientBalance.day)
            ).label("next")
        ).order_by(
            ClientBalance.client_id,
            ClientBalance.day,
        ).subquery("pre_periodized")

        periodized = select(
            pre_periodized.c.client_id,
            pre_periodized.c.day.label("period_start"),
            case(
                (pre_periodized.c.next == 0, pre_periodized.c.day),
                else_=pre_periodized.c.day,
            ).label("period_end"),
            pre_periodized.c.period,
            pre_periodized.c.balance,
        ).where(
            pre_periodized.c.balance > 0
        ).subquery("periodized")

        return select(
            periodized.c.client_id,
            func.first_value(
                periodized.c.period_start
            ).over(
                partition_by=periodized.c.period,
            ).label("period_start"),
            func.last_value(
                periodized.c.period_end
            ).over(
                partition_by=periodized.c.period,
            ).label("period_end"),
            func.avg(
                periodized.c.balance
            ).over(
                partition_by=periodized.c.period,
            ).label("avg_balance_within_period"),
        ).order_by(
            periodized.c.client_id,
            periodized.c.period,
            periodized.c.period_start,
        ).distinct(
            periodized.c.client_id,
            periodized.c.period,
        )
