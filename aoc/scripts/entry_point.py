import importlib
import json
import os
import shutil

import click
import jinja2
import requests

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
@click.option("--session", default=None)
def new(day=None, session=None):
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
    data_folder = os.path.join(DATA_FOLDER, f"day{day}")
    os.mkdir(data_folder)
    download_input_for_day(day, session=session)


def download_input_for_day(day, *, session=None):
    data_folder = os.path.join(DATA_FOLDER, f"day{day}")
    if session is None:
        session = get_session()
    with open(os.path.join(data_folder, "input"), "wb") as f:
        for chunk in requests.get(
            f"https://adventofcode.com/2020/day/{day}/input",
            cookies={"session": session},
            stream=True,
        ).iter_content(chunk_size=1024):
            f.write(chunk)


def get_session():
    with open(os.path.expanduser("~/.aoc")) as f:
        config = json.load(f)
    session = config["session"]
    return session


@cli.command()
@click.option("--day", default=None)
@click.option("--session", default=None)
def download(day=None, session=None):
    if day is None:
        day = get_last_day()
    download_input_for_day(day, session=session)


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
