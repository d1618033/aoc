from typing import TypeVar, Callable

Value = TypeVar("Value")


class Option:
    def __init__(self, value: Value) -> None:
        ...

    def or_call(self, callable: Callable[[], Value]) -> "Option":
        ...

    def get_or(self, value: Value) -> Value:
        ...
