import importlib
import os
import shutil

import click
import jinja2

from aoc import utils
from aoc.utils import get_day_from_file_name

MAIN_FOLDER = os.path.join(os.path.dirname(__file__), "..")
TESTS_FOLDER = os.path.join(MAIN_FOLDER, "..", "tests")
DATA_FOLDER = os.path.join(MAIN_FOLDER, "..", "data")


@click.group()
def cli():
    pass


@cli.command()
@click.argument("day")
@click.option("--input", "input_file", default=None)
def solve(day, input_file=None):
    module = importlib.import_module(f"aoc.day{day}")
    if input_file:
        utils.input_file_ctx.set(os.path.abspath(input_file))
    utils.day_ctx.set(day)
    module.main()


@cli.command()
@click.option("--day", default=None)
def new(day=None):
    if day is None:
        day = get_last_day() + 1
    click.echo(f"Making day{day}")
    jinja_env = jinja2.Environment(
        loader=jinja2.PackageLoader("aoc", "templates"),
        keep_trailing_newline=True,
    )
    kwargs = {"day_number": day}
    with open(os.path.join(MAIN_FOLDER, f"day{day}.py"), "w") as f:
        f.write(jinja_env.get_template("day.jinja").render(**kwargs))
    with open(os.path.join(TESTS_FOLDER, f"test_day{day}.py"), "w") as f:
        f.write(jinja_env.get_template("test_day.jinja").render(**kwargs))
    os.mkdir(os.path.join(DATA_FOLDER, f"day{day}"))


def get_all_days():
    return [
        get_day_from_file_name(file)
        for file in os.listdir(MAIN_FOLDER)
        if file.startswith("day")
    ]


@cli.command()
@click.option("--day", default=None)
def rm(day=None):
    if day is None:
        day = get_last_day()
    os.remove(os.path.join(MAIN_FOLDER, f"day{day}.py"))
    os.remove(os.path.join(TESTS_FOLDER, f"test_day{day}.py"))
    shutil.rmtree(os.path.join(DATA_FOLDER, f"day{day}"))


def get_last_day():
    return max(get_all_days())
