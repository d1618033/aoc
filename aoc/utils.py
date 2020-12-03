import enum
import inspect
import os
import re
import typing
from contextvars import ContextVar

input_file_ctx = ContextVar("input_file", default=None)


def get_file_path(
    file_name: typing.Optional[str] = None, *, day: typing.Optional[int] = None
) -> str:
    if file_name is None:
        file_name = input_file_ctx.get()
        if file_name is None:
            file_name = "input"

    if os.path.isabs(file_name):
        return file_name

    if day is None:
        for frame in inspect.stack():
            if "day" in frame.filename:
                day = int(unwrap(re.search(r"day(\d+)", frame.filename)).groups()[0])
                break
        else:
            day = 1
    return os.path.join(os.path.dirname(__file__), "..", "data", f"day{day}", file_name)


def load_input(file_name=None, *, day=None):
    with open(get_file_path(file_name, day=day)) as file:
        return file.read().splitlines()


class StringEnum(str, enum.Enum):
    pass


GenericType = typing.TypeVar("GenericType")


def unwrap(element: typing.Optional[GenericType]) -> GenericType:
    if element is None:
        raise ValueError("Unexpected None")
    return element
