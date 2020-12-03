import enum
import os

import typing


def load(file_name, *, day):
    full_path = os.path.join(
        os.path.dirname(__file__), "..", "data", f"day{day}", file_name
    )
    with open(full_path) as file:
        return file.read().splitlines()


class StringEnum(str, enum.Enum):
    pass


GenericType = typing.TypeVar("GenericType")


def unwrap(element: typing.Optional[GenericType]) -> GenericType:
    if element is None:
        raise ValueError("Unexpected None")
    return element
