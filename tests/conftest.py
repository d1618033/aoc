import pytest

from aoc import utils


@pytest.fixture(autouse=True)
def input_file():
    utils.input_file_ctx.set("example")
