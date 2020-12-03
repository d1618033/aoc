import pytest
from typeguard.importhook import install_import_hook

install_import_hook("aoc")

from aoc import utils


@pytest.fixture(autouse=True)
def input_file():
    utils.input_file_ctx.set("example")
