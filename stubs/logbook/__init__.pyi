from typing import Any


DEBUG: int


class Logger:
    def __init__(self, name: str):
        ...

    def debug(self, message: str) -> None:
        ...


class StreamHandler:
    def __init__(self, stream: Any, level: int) -> None:
        ...

    def push_application(self) -> None:
        ...