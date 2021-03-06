import enum
import inspect
import operator
import re
from contextlib import ExitStack, contextmanager
from contextvars import ContextVar
from functools import reduce
from pathlib import Path
from typing import Final, Optional, TypeVar

import logbook
from fn.func import curried
from fn.monad import Option

input_file_ctx: ContextVar[Optional[Path]] = ContextVar("input_file", default=None)
day_ctx: ContextVar[Optional[int]] = ContextVar("day", default=None)


MAIN_FOLDER: Final[Path] = Path(__file__).parent
TESTS_FOLDER: Final[Path] = MAIN_FOLDER.parent / "tests"
DATA_FOLDER: Final[Path] = MAIN_FOLDER.parent / "data"

logger: Final = logbook.Logger(__name__)


def print_(*message):
    logger.debug(" ".join(map(str, message)))


@contextmanager
def set_and_reset(contextvar, value):
    token = contextvar.set(value)
    yield
    contextvar.reset(token)


@contextmanager
def setting_defaults(*, input_file: Optional[Path] = None, day: Optional[int] = None):
    variables_and_contexts = [
        (input_file, input_file_ctx),
        (day, day_ctx),
    ]
    with ExitStack() as stack:
        for value, contextvar in variables_and_contexts:
            if value:
                stack.enter_context(set_and_reset(contextvar, value))
        yield


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


def load_input(
    file_path: Optional[Path] = None,
    *,
    day: Optional[int] = None,
    delim="\n",
    strip=True,
    skip_empty=True,
):
    lines = _get_input_file_path(file_path, day).read_text().split(delim)
    if strip:
        lines = [line.strip() for line in lines]
    if skip_empty:
        lines = [line for line in lines if line]
    return lines


def load_ints(
    file_path: Optional[Path] = None, *, day: Optional[int] = None, delim="\n"
):
    return list(
        map(int, load_input(file_path=file_path, day=day, delim=delim, strip=True))
    )


class StringEnum(str, enum.Enum):
    pass


class MultiValueEnum(enum.Enum):
    def __new__(cls, *values):
        obj = object.__new__(cls)
        # first value is canonical value
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj  # pylint: disable=no-member
        obj._all_values = values
        return obj


GenericType = TypeVar("GenericType")


def unwrap(element: Optional[GenericType], item: Optional[str] = "item") -> GenericType:
    if element is None:
        raise ValueError(f"{item} is unexpectedly None")
    return element


def _compose2(f, g):
    def new_func(*args, **kwargs):
        return f(g(*args, **kwargs))

    return new_func


def compose(*functions):
    return reduce(_compose2, functions)


def raise_if_not(predicate, exception, *args, **kwargs):
    if not predicate:
        raise exception(*args, **kwargs)


@curried
def obj_inplace_op(op, obj, attr, value):
    setattr(obj, attr, op(getattr(obj, attr), value))


iadd = obj_inplace_op(operator.iadd)  # pylint: disable=no-value-for-parameter
isub = obj_inplace_op(operator.isub)  # pylint: disable=no-value-for-parameter
