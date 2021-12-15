import datetime
import enum
import inspect
import operator
import re
from contextlib import ExitStack, contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import Final, Optional, TypeVar

import logbook
from fn.func import curried
from fn.monad import Option

input_file_ctx: ContextVar[Optional[Path]] = ContextVar("input_file", default=None)
day_ctx: ContextVar[Optional[int]] = ContextVar("day", default=None)
year_ctx: ContextVar[Optional[int]] = ContextVar("year", default=None)


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


def _get_year_from_caller() -> Optional[int]:
    for frame in inspect.stack():
        if "day" in frame.filename:
            return get_year_from_file_name(frame.filename)
    return None


def _get_day_from_caller() -> Optional[int]:
    for frame in inspect.stack():
        if "day" in frame.filename:
            return get_day_from_file_name(frame.filename)
    return None


def get_year_from_file_name(file_name: str) -> int:
    return int(unwrap(re.search(r"year(\d+)", file_name)).groups()[0])


def get_day_from_file_name(file_name: str) -> int:
    return int(unwrap(re.search(r"day(\d+)", file_name)).groups()[0])


def _get_input_file_path(
    maybe_file_path: Optional[Path] = None,
    maybe_day: Optional[int] = None,
    maybe_year: Optional[int] = None,
) -> Path:
    file_path: Path = (
        Option(maybe_file_path).or_call(input_file_ctx.get).get_or(Path("input"))
    )
    if file_path.is_absolute():
        return file_path
    day = Option(maybe_day).or_call(day_ctx.get).or_call(_get_day_from_caller).get_or(1)
    year = (
        Option(maybe_year)
        .or_call(year_ctx.get)
        .or_call(_get_year_from_caller)
        .get_or(datetime.datetime.now().year)
    )
    return Path(__file__).parent.parent.joinpath(
        "data", f"year{year}", f"day{day}", file_path
    )


def load_input(
    file_path: Optional[Path] = None,
    *,
    day: Optional[int] = None,
    year: Optional[int] = None,
    delim="\n",
    strip=True,
    skip_empty=True,
):
    lines = _get_input_file_path(file_path, day, year).read_text().split(delim)
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


def load_board_of_ints(
    file_path: Optional[Path] = None, *, day: Optional[int] = None, delim="\n"
):
    return [
        list(map(int, line))
        for line in load_input(file_path=file_path, day=day, delim=delim, strip=True)
    ]


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
    return obj


iadd = obj_inplace_op(operator.iadd)  # pylint: disable=no-value-for-parameter
isub = obj_inplace_op(operator.isub)  # pylint: disable=no-value-for-parameter


def sign(x):
    return 1 if x > 0 else 0 if x == 0 else -1


def get_neighbors(row, col, num_rows, num_cols, diagonal=True):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if not diagonal and i != 0 and j != 0:
                continue
            if 0 <= i + row < num_rows and 0 <= j + col < num_cols:
                yield (i + row, j + col)


@dataclass
class Cell:
    row_number: int
    col_number: int
    value: int
    board: "Board"

    def get_neighbors(self, diagonal=True):
        for row, col in get_neighbors(
            self.row_number,
            self.col_number,
            self.board.num_rows,
            self.board.num_cols,
            diagonal=diagonal,
        ):
            yield self.board.get_cell(row, col)

    def __hash__(self):
        return hash((self.row_number, self.col_number))


class Board:
    def __init__(self, data):
        self.cells = [
            [
                Cell(row_number=i, col_number=j, board=self, value=col)
                for j, col in enumerate(row)
            ]
            for i, row in enumerate(data)
        ]

    def get_cell(self, row_number, col_number) -> Cell:
        return self.cells[row_number][col_number]

    @property
    def num_rows(self):
        return len(self.cells)

    @property
    def num_cols(self):
        return len(self.cells[0])

    @property
    def num_cells(self):
        return self.num_rows * self.num_cols

    @property
    def cells_flat(self):
        for row in self.cells:
            for cell in row:
                yield cell
