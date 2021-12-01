import re
from math import prod
from typing import List, Optional

from pydantic import BaseModel

from aoc.utils import load_input


class Range(BaseModel):
    lower: int
    upper: int

    def in_range(self, value):
        return self.lower <= value <= self.upper


class Field(BaseModel):
    name: str
    ranges: List[Range]

    def in_range(self, value):
        return any(range_.in_range(value) for range_ in self.ranges)


class Ticket(BaseModel):
    values: List[int]


class Data(BaseModel):
    field_definitions: List[Field]
    your_ticket: Optional[Ticket]
    nearby_tickets: List[Ticket]


def part1():
    data = load_data()
    return sum(
        value
        for ticket in data.nearby_tickets
        for value in ticket.values
        if not any(
            range_.in_range(value)
            for field_definition in data.field_definitions
            for range_ in field_definition.ranges
        )
    )


def load_data():
    field_definition = re.compile(
        r"^(?P<name>[\w\s]+):\s*"
        r"(?P<lower_1>\d+)-(?P<upper_1>\d+)\s*"
        r"or\s*"
        r"(?P<lower_2>\d+)-(?P<upper_2>\d+)$"
    )
    data = Data(field_definitions=[], your_ticket=None, nearby_tickets=[])
    lines = iter(load_input())
    while (line := next(lines, None)) is not None:
        if match := field_definition.match(line):
            matches = match.groupdict()
            data.field_definitions.append(
                Field(
                    name=matches["name"],
                    ranges=[
                        Range(lower=matches[f"lower_{i}"], upper=matches[f"upper_{i}"])
                        for i in [1, 2]
                    ],
                )
            )
        elif line.startswith("your ticket"):
            line = next(lines)
            data.your_ticket = Ticket(values=line.split(","))
        elif line.startswith("nearby tickets"):
            for line in lines:
                data.nearby_tickets.append(Ticket(values=line.split(",")))
    assert data.your_ticket
    assert data.field_definitions
    assert data.nearby_tickets
    return data


def get_field_order(data):
    valid_tickets = [
        ticket
        for ticket in data.nearby_tickets
        if all(
            any(
                range_.in_range(value)
                for field_definition in data.field_definitions
                for range_ in field_definition.ranges
            )
            for value in ticket.values
        )
    ]
    assert valid_tickets
    options_for_fields = [
        (field, set(range(len(data.your_ticket.values))))
        for field in data.field_definitions
    ]
    for ticket in valid_tickets:
        for i, value in enumerate(ticket.values):
            for field, options in options_for_fields:
                if not field.in_range(value):
                    options.remove(i)
    while True:
        one_options = [
            list(options)[0] for _, options in options_for_fields if len(options) == 1
        ]
        more_than_one = [
            options for _, options in options_for_fields if len(options) > 1
        ]
        if len(more_than_one) == 0:
            break
        for options in more_than_one:
            for option in one_options:
                options.discard(option)
    field_order = [
        field.name
        for field, options in sorted(options_for_fields, key=lambda x: list(x[1])[0])
    ]
    return field_order


def part2():
    data = load_data()
    return prod(
        value
        for field, value in zip(get_field_order(data), data.your_ticket.values)
        if field.startswith("departure")
    )


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
