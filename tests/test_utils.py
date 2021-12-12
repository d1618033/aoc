import io
import re

import logbook
import pytest

from aoc.utils import get_neighbors, print_


def test_print_():
    sio = io.StringIO()
    logbook.StreamHandler(sio).push_application()

    class World:
        def __str__(self):
            return "world"

    print_("Hello", World())
    sio.seek(0)
    assert re.match(
        r"\[\d+\-\d+\-\d+ \d+:\d+:\d+\.\d+\] DEBUG: aoc.utils: Hello world", sio.read()
    )


@pytest.mark.parametrize(
    "row,col,num_rows,num_cols,diagonal,expected",
    [
        (0, 0, 3, 3, True, [(0, 1), (1, 0), (1, 1)]),
        (0, 1, 3, 3, True, [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)]),
        (0, 2, 3, 3, True, [(0, 1), (1, 1), (1, 2)]),
        (1, 0, 3, 3, True, [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)]),
        (
            1,
            1,
            3,
            3,
            True,
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
        ),
        (1, 2, 3, 3, True, [(0, 1), (0, 2), (1, 1), (2, 1), (2, 2)]),
        (2, 0, 3, 3, True, [(1, 0), (1, 1), (2, 1)]),
        (2, 1, 3, 3, True, [(1, 0), (1, 1), (1, 2), (2, 0), (2, 2)]),
        (2, 2, 3, 3, True, [(1, 1), (1, 2), (2, 1)]),
        (0, 0, 3, 3, False, [(0, 1), (1, 0)]),
        (0, 1, 3, 3, False, [(0, 0), (0, 2), (1, 1)]),
        (0, 2, 3, 3, False, [(0, 1), (1, 2)]),
        (1, 0, 3, 3, False, [(0, 0), (1, 1), (2, 0)]),
        (1, 1, 3, 3, False, [(0, 1), (1, 0), (1, 2), (2, 1)]),
        (1, 2, 3, 3, False, [(0, 2), (1, 1), (2, 2)]),
        (2, 0, 3, 3, False, [(1, 0), (2, 1)]),
        (2, 1, 3, 3, False, [(1, 1), (2, 0), (2, 2)]),
        (2, 2, 3, 3, False, [(1, 2), (2, 1)]),
    ],
)
def test_get_neighbors(
    row, col, num_rows, num_cols, diagonal, expected
):  # pylint: disable=too-many-arguments
    assert sorted(get_neighbors(row, col, num_rows, num_cols, diagonal)) == sorted(
        expected
    )
