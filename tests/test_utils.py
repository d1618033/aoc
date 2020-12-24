import io
import re

import logbook

from aoc.utils import print_


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
