import re
from typing import List, Optional, Set, Tuple

from pydantic import BaseModel, Field, ValidationError, validator
from traceback_with_variables import iter_tb_lines

from aoc.utils import StringEnum, load_input, logger

Color = str
Id = str


class EyeColor(StringEnum):
    amber = "amb"
    blue = "blu"
    brown = "brn"
    grey = "gry"
    green = "grn"
    hazel = "hzl"
    other = "oth"

    def __str__(self):
        return self.value

    def __repr__(self):
        return repr(str(self))


class Unit(StringEnum):
    centimeters = "cm"
    inches = "in"


class Height(BaseModel):
    unit: Unit
    value: int

    @validator("value")
    def validate_value(cls, value, values, **kwargs):
        unit: Unit = values["unit"]
        if unit == unit.centimeters:
            raise_if_not(150 <= value <= 193, ValueError, f"Bad height {value} for cm")
        elif unit == unit.inches:
            raise_if_not(
                59 <= value <= 76, ValueError, f"Bad height {value} for inches"
            )
        return value

    def __repr__(self):
        return repr(str(self))

    def __str__(self):
        return f"{self.value}{self.unit.value}"


class SimplePassportModel(BaseModel):
    byr: int
    iyr: int
    eyr: int
    hgt: str
    hcl: str
    ecl: str
    pid: str
    cid: Optional[str]


class AdvancedPassportModel(BaseModel):
    byr: int = Field(ge=1920, le=2002)
    iyr: int = Field(ge=2010, le=2020)
    eyr: int = Field(ge=2020, le=2030)
    hgt: str
    hcl: Color = Field(regex=r"^#[0-9a-f]{6}$")
    ecl: EyeColor
    pid: Id = Field(regex=r"^\d{9}$")
    cid: Id = Field(default=None)

    @validator("hgt")
    def validate_height(cls, height_str):
        if match := re.match(r"^(?P<value>\d+)(?P<unit>in|cm)$", height_str):
            return Height(**match.groupdict())
        raise ValueError(f"Unknown height format {height_str}")


def try_else(func, exception=Exception, default=None, log_error=False, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except exception as e:
        if log_error:
            logger.exception(f"Failed to run func {func}" + "\n".join(iter_tb_lines(e)))
        return default
    except Exception:
        logger.exception(f"Failed to run func {func}")


def raise_if_not(predicate, exception, *args, **kwargs):
    if not predicate:
        raise exception(*args, **kwargs)


def parse_input(model):
    raw_passports = load_input(delim="\n\n")
    return [
        try_else(
            parse_single_passport,
            exception=ValidationError,
            default=None,
            log_error=False,
            raw_passport=raw_passport,
            model=model,
        )
        for raw_passport in raw_passports
    ]


def parse_single_passport(raw_passport, model):
    items = re.split(r"\s+", raw_passport)
    data = dict(item.split(":") for item in items if item)
    return model(**data)


def num_valid(model):
    return sum(passport is not None for passport in parse_input(model))


def part1():
    return num_valid(SimplePassportModel)


def part2():
    return num_valid(AdvancedPassportModel)


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
