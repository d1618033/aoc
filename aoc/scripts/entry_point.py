import importlib
import json
import shutil
from pathlib import Path

import click
import jinja2
import requests

from aoc.utils import (
    DATA_FOLDER,
    MAIN_FOLDER,
    TESTS_FOLDER,
    get_day_from_file_name,
    setting_defaults,
)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("day")
@click.option("--input", "input_file", default=None)
def solve(day, input_file=None):
    if input_file is not None:
        input_file = Path(input_file).resolve()
    with setting_defaults(input_file=input_file, day=day):
        module = importlib.import_module(f"aoc.day{day}")
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
    MAIN_FOLDER.joinpath(f"day{day}.py").write_text(
        jinja_env.get_template("day.jinja").render(**kwargs)
    )
    TESTS_FOLDER.joinpath(f"test_day{day}.py").write_text(
        jinja_env.get_template("test_day.jinja").render(**kwargs)
    )
    data_folder = DATA_FOLDER.joinpath(f"day{day}")
    data_folder.mkdir()
    download_input_for_day(day, session=session)


def download_input_for_day(day, *, session=None):
    data_folder = DATA_FOLDER.joinpath(f"day{day}")
    if session is None:
        session = get_session()
    with data_folder.joinpath("input").open("wb") as f:
        for chunk in requests.get(
            f"https://adventofcode.com/2020/day/{day}/input",
            cookies={"session": session},
            stream=True,
        ).iter_content(chunk_size=1024):
            f.write(chunk)


def get_session():
    config = json.loads(Path("~/.aoc").expanduser().read_text())
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
    return [get_day_from_file_name(str(file)) for file in MAIN_FOLDER.glob("day*.py")]


@cli.command()
@click.option("--day", default=None)
def rm(day=None):
    if day is None:
        day = get_last_day()
    MAIN_FOLDER.joinpath(f"day{day}.py").unlink()
    TESTS_FOLDER.joinpath(f"test_day{day}.py").unlink()
    shutil.rmtree(DATA_FOLDER.joinpath(f"day{day}"))


def get_last_day():
    return max(get_all_days())
