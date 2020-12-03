import importlib
import os

import click

from aoc import utils


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
