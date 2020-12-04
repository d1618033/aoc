from pathlib import Path
import sys

import pytest
from logbook import DEBUG, StreamHandler

from aoc import utils


@pytest.fixture(autouse=True, scope="session")
def logging():
    StreamHandler(sys.stdout, level=DEBUG).push_application()


@pytest.fixture(autouse=True)
def input_file(request):
    file_name = "example"
    if marker := request.node.get_closest_marker("input_file"):
        file_name = marker.args[0]
    utils.input_file_ctx.set(Path(file_name))

