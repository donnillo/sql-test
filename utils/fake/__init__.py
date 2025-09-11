import random
from collections.abc import Generator


def finite_sequence_gen[T](
    *items: T,
    loss_rate: float | None = None,
) -> Generator[T, None, None]:
    seq = list(items)
    random.shuffle(seq)
    length = len(seq)
    if loss_rate and 0 < loss_rate < 1:
        seq = seq[:random.randint(int((1 - loss_rate) * length), length)]
    while seq:
        yield seq.pop()
