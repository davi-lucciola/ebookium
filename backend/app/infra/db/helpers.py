from typing import cast

from sqlalchemy import Result


def extract_data_and_total[T](
    result: Result[tuple[T, int]],
) -> tuple[list[T], int]:
    rows = result.all()
    data = [cast(T, row[0]) for row in rows]
    total = cast(int, rows[0][1]) if rows else 0

    return data, total
