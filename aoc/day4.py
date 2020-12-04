import re
from typing import Dict, Optional, Tuple, Type, cast

from pydantic import BaseModel, Field, ValidationError, validate_model, validator

from aoc.utils import StringEnum, load_input, raise_if_not

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


class Unit(StringEnum):
    centimeters = "cm"
    inches = "in"


class Height(BaseModel):
    unit: Unit
    value: int

    @classmethod
    @validator("value")
    def validate_value(cls, value, values):
        unit: Unit = values["unit"]
        if unit == unit.centimeters:
            raise_if_not(150 <= value <= 193, ValueError, f"Bad height {value} for cm")
        elif unit == unit.inches:
            raise_if_not(
                59 <= value <= 76, ValueError, f"Bad height {value} for inches"
            )
        return value


class SimplePassportModel(BaseModel):
    byr: str
    iyr: str
    eyr: str
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

    @classmethod
    @validator("hgt")
    def validate_height(cls, height_str):
        if match := re.match(r"^(?P<value>\d+)(?P<unit>in|cm)$", height_str):
            return Height(**match.groupdict())
        raise ValueError(f"Unknown height format {height_str}")


def validate_all_passports(model):
    raw_passports = load_input(delim="\n\n")
    return [validate_passport(model, raw_passport) for raw_passport in raw_passports]


def validate_passport(
    model: Type[BaseModel], raw_passport: str
) -> Optional[ValidationError]:
    items = re.split(r"\s+", raw_passport)
    data: Dict[str, str] = dict(
        cast(Tuple[str, str], item.split(":")) for item in items if item
    )
    _, _, errors = validate_model(model, data)
    return errors


def num_valid(model):
    return sum(
        validation_errors is None for validation_errors in validate_all_passports(model)
    )


def part1():
    return num_valid(SimplePassportModel)


def part2():
    return num_valid(AdvancedPassportModel)


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
