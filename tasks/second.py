import model.clients
from model.clients import ClientBalance
from tasks.common import Database, TaskMixin
from utils.dates import last_n_months
from utils.fake.clients import get_clients, get_balance


class TaskTwo(TaskMixin):
    Base = model.clients.Base
    target = ClientBalance

    def generate_data(self):
        clients = [*get_clients()]
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
    def query(self):
        pass
