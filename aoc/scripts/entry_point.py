import importlib
import json
import shutil
from pathlib import Path

import click
import jinja2
import requests
from typeguard.importhook import install_import_hook

install_import_hook("aoc")

from aoc import utils
from aoc.utils import get_day_from_file_name

MAIN_FOLDER: Path = Path(__file__).parent.parent
TESTS_FOLDER: Path = MAIN_FOLDER.parent / "tests"
DATA_FOLDER: Path = MAIN_FOLDER.parent / "data"


@click.group()
def cli():
    pass


@cli.command()
@click.argument("day")
@click.option("--input", "input_file", default=None)
def solve(day, input_file=None):
    module = importlib.import_module(f"aoc.day{day}")
    if input_file:
        utils.input_file_ctx.set(Path(input_file).absolute())
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
    with MAIN_FOLDER.joinpath(f"day{day}.py").open("w") as f:
        f.write(jinja_env.get_template("day.jinja").render(**kwargs))
    with TESTS_FOLDER.joinpath(f"test_day{day}.py").open("w") as f:
        f.write(jinja_env.get_template("test_day.jinja").render(**kwargs))
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
    with Path("~/.aoc").expanduser().open() as f:
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
