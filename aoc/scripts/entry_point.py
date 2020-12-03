import importlib
import os

import click

from aoc import utils


@click.group()
def cli():
    pass


@cli.command()
@click.option("--day")
@click.option("--input", "input_file")
def solve(day, input_file):
    module = importlib.import_module(f"aoc.day{day}")
    utils.input_file_ctx.set(os.path.abspath(input_file))
    module.main()
