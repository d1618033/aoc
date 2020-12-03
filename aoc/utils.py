import enum
import inspect
import re
from contextvars import ContextVar
from functools import reduce
from pathlib import Path
from typing import Optional, TypeVar

from fn.monad import Option

input_file_ctx: ContextVar[Optional[Path]] = ContextVar("input_file", default=None)
day_ctx: ContextVar[Optional[int]] = ContextVar("day", default=None)


def _get_day_from_caller() -> Optional[int]:
    for frame in inspect.stack():
        if "day" in frame.filename:
            return get_day_from_file_name(frame.filename)
    return None


def get_day_from_file_name(file_name: str) -> int:
    return int(unwrap(re.search(r"day(\d+)", file_name)).groups()[0])


def _get_input_file_path(
    maybe_file_path: Optional[Path] = None,
    maybe_day: Optional[int] = None,
) -> Path:
    file_path: Path = (
        Option(maybe_file_path).or_call(input_file_ctx.get).get_or(Path("input"))
    )
    if file_path.is_absolute():
        return file_path
    day = Option(maybe_day).or_call(day_ctx.get).or_call(_get_day_from_caller).get_or(1)
    return Path(__file__).parent.parent.joinpath("data", f"day{day}", file_path)


def load_input(file_path: Optional[Path] = None, *, day: Optional[int] = None):
    with _get_input_file_path(file_path, day).open() as file:
        return file.read().splitlines()


class StringEnum(str, enum.Enum):
    pass


GenericType = TypeVar("GenericType")


def unwrap(element: Optional[GenericType]) -> GenericType:
    if element is None:
        raise ValueError("Unexpected None")
    return element


def _compose2(f, g):
    def new_func(*args, **kwargs):
        return f(g(*args, **kwargs))

    return new_func


def compose(*functions):
    return reduce(_compose2, functions)
