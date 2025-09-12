from collections.abc import Sequence

from tabulate import tabulate
import sqlalchemy


def render_table(
    rows: Sequence[sqlalchemy.engine.Row], *,
    max_rows: int = 31,
    title: str | None = None
):
    headers = rows[0]._fields

    if (skipped := abs(min(max_rows - len(rows), 0))) > 1:
        rendered_rows = [
            *rows[:max_rows // 2],
            tuple(None for _ in headers),
            *rows[max_rows // 2 + skipped + 1:]
        ]
    else:
        rendered_rows = rows

    table = tabulate(
        rendered_rows,
        headers=headers,
        tablefmt="rounded_outline",
        missingval="\u00b7" * 3,
        floatfmt=",.2f",
    )

    width = len(table.partition("\n")[0])
    if title:
        print(f"{f" {title} ":\u2500^{width}}")
    print(table)
    if skipped > 1:
        print(f"{skipped} rows skipped")
