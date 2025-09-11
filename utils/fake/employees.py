import random
import datetime
from collections.abc import Generator

from model.employees import Presence, Employee
from utils.fake import finite_sequence_gen


def split_time(value: float) -> tuple[int, int, int]:
    return (
        max(min(int(value), 23), 5),
        int(value % 1 * 60),
        random.randint(0, 59),
    )


SIGMAS = (0.8, 1.1, 4, 2.5)
EARLY = (8.5, 9.5, 10, 11)
LATE = (18, 18.5, 19, 20)


def get_presence() -> Presence:
    starts, ends = [
        [split_time(random.gauss(mu, sigma))
         for mu, sigma in zip(hours, SIGMAS)]
        for hours in (EARLY, LATE)
    ]
    start, end = sorted((random.choice(starts), random.choice(ends)))
    return Presence(
        arrival=datetime.time(*start),
        departure=datetime.time(*end)
    )


def get_employee() -> Generator[Employee, None, None]:
    for name in finite_sequence_gen(
        "Александр",
        "Анастасия",
        "Данила",
        "Герман",
        "Оскар",
        "Эльвира",
        "Антон",
        "Михаил",
        "Максим",
        "Сергей",
        "Дмитрий",
        "Владимир",
        loss_rate=0.2
    ):
        yield Employee(name)
