import enum
import inspect
import os
import re
import typing
from contextvars import ContextVar
from functools import reduce

from fn.monad import Option

input_file_ctx = ContextVar("input_file", default=None)
day_ctx = ContextVar("day", default=None)


def _get_day_from_caller() -> typing.Optional[int]:
    for frame in inspect.stack():
        if "day" in frame.filename:
            return get_day_from_file_name(frame.filename)
    return None


def get_day_from_file_name(file_name: str) -> int:
    return int(unwrap(re.search(r"day(\d+)", file_name)).groups()[0])


def _get_file_path(
    maybe_file_name: typing.Optional[str] = None, maybe_day: typing.Optional[int] = None
) -> str:
    file_name = Option(maybe_file_name).or_call(input_file_ctx.get).get_or("input")
    if os.path.isabs(file_name):
        return file_name
    day = Option(maybe_day).or_call(day_ctx.get).or_call(_get_day_from_caller).get_or(1)
    return os.path.join(os.path.dirname(__file__), "..", "data", f"day{day}", file_name)


def load_input(file_name=None, *, day=None):
    with open(_get_file_path(file_name, day)) as file:
        return file.read().splitlines()


class StringEnum(str, enum.Enum):
    pass


GenericType = typing.TypeVar("GenericType")


def unwrap(element: typing.Optional[GenericType]) -> GenericType:
    if element is None:
        raise ValueError("Unexpected None")
    return element


def _compose2(f, g):
    def new_func(*args, **kwargs):
        return f(g(*args, **kwargs))

    return new_func


def compose(*functions):
    return reduce(_compose2, functions)
