import random
from decimal import Decimal
from collections.abc import Generator

from model.clients import Client
from utils.fake import finite_sequence_gen


def get_balance():
    mu = 10_000 * random.randrange(1, 300)
    sigma = random.randrange(90, 120) / 100 * mu
    while True:
        rounder = random.choices(
            (-6, -5, -4, -3, -2, -1, 0, 1, 2),
            (.9, .5, .5,  4,  2,  2, 3, 1, 3),
        )[0]
        yield Decimal(str(
            round(max(random.gauss(mu, sigma), 0), rounder)
        ))


def get_clients() -> Generator[Client, None, None]:
    for name in finite_sequence_gen(
        "Соломон Важнович",
        "Иван Аристократов",
        "Татьяна Скоробогатько",
        "Роберт Рокфеллеров",
        "Марат Решайло",
        "Жан Нуворишев",
    ):
        yield Client(name)
