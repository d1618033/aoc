import datetime
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

NOW = datetime.datetime.now()


@click.group()
def cli():
    pass


@cli.command()
@click.option("--day", default=None)
@click.option("--year", default=NOW.year)
@click.option("--part", default=None)
@click.option("--input", "input_file", default=None)
def solve(year, day=None, part=None, input_file=None):
    if day is None:
        day = get_last_day(year)
    if input_file is not None:
        input_file = Path(input_file).resolve()
    with setting_defaults(input_file=input_file, day=day):
        module = importlib.import_module(f"aoc.year{year}.day{day}")
        if part:
            print(getattr(module, f"part{part}")())
        else:
            module.main()


@cli.command()
@click.option("--day", default=None)
@click.option("--year", default=NOW.year)
@click.option("--session", default=None)
def new(year, day=None, session=None):
    if day is None:
        day = get_last_day() + 1
    click.echo(f"Making day{day}")
    jinja_env = jinja2.Environment(
        loader=jinja2.PackageLoader("aoc", "templates"),
        keep_trailing_newline=True,
    )
    kwargs = {"day_number": day, "year_number": year}
    MAIN_FOLDER.joinpath(f"year{year}").joinpath(f"day{day}.py").write_text(
        jinja_env.get_template("day.jinja").render(**kwargs)
    )
    TESTS_FOLDER.joinpath(f"year{year}").joinpath(f"test_day{day}.py").write_text(
        jinja_env.get_template("test_day.jinja").render(**kwargs)
    )
    data_folder = DATA_FOLDER.joinpath(f"year{year}").joinpath(f"day{day}")
    data_folder.mkdir(exist_ok=True)
    download_input_for_day(year, day, session=session)
    data_folder.joinpath("example").touch()


def download_input_for_day(year, day, *, session=None):
    data_folder = DATA_FOLDER.joinpath(f"year{year}").joinpath(f"day{day}")
    if session is None:
        session = get_session()
    with data_folder.joinpath("input").open("wb") as f:
        for chunk in requests.get(
            f"https://adventofcode.com/{year}/day/{day}/input",
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
@click.option("--year", default=NOW.year)
@click.option("--session", default=None)
def download(year, day=None, session=None):
    if day is None:
        day = get_last_day(year) + 1
    download_input_for_day(year, day, session=session)


def get_all_days(year):
    return [
        get_day_from_file_name(str(file))
        for file in MAIN_FOLDER.glob("year{year}/day*.py")
    ]


@cli.command()
@click.option("--day", default=None)
@click.option("--year", default=NOW.year)
def rm(year, day=None):
    if day is None:
        day = get_last_day(year)
    MAIN_FOLDER.joinpath(f"year{year}").joinpath(f"day{day}.py").unlink()
    TESTS_FOLDER.joinpath(f"year{year}").joinpath(f"test_day{day}.py").unlink()
    shutil.rmtree(DATA_FOLDER.join(f"year{year}").joinpath(f"day{day}"))


def get_last_day(year):
    days = get_all_days(year)
    if not days:
        return 0
    return max(days)
