import math
from dataclasses import dataclass
from itertools import islice
from typing import List
import abc
from aoc.utils import load_input


def decode(hexadecimal_chars):
    for char in hexadecimal_chars:
        decimal = int(char, 16)
        binary = bin(decimal)[2:]
        if len(binary) < 4:
            binary = "0" * (4 - len(binary)) + binary
        for c in binary:
            yield c


@dataclass
class Packet:
    version: int
    type_id: int


@dataclass
class LiteralPacket(Packet):
    number: int

    @classmethod
    def from_stream(cls, version, type_id, data):
        num_parts = []
        while True:
            flag = get_bin(data, 1)
            num_part = get(data, 4)
            num_parts.append(num_part)
            if flag == 0:
                break
        number = int("".join(num_parts), 2)
        return cls(version=version, type_id=type_id, number=number)


@dataclass
class OperatorPacket(Packet):
    length_type_id: int
    sub_packets: List[Packet]

    @classmethod
    def from_stream(cls, version, type_id, data):
        length_type_id = get_bin(data, 1)
        if length_type_id == 0:
            total_length = get_bin(data, 15)
            sub_packets_data = iter(get(data, total_length))
            sub_packets = []
            while True:
                try:
                    sub_packets.append(parse_packets(sub_packets_data))
                except StopIteration:
                    break
        else:
            total_packets = get_bin(data, 11)
            sub_packets = []
            for _ in range(total_packets):
                sub_packets.append(parse_packets(data))
        return cls(
            version=version,
            type_id=type_id,
            length_type_id=length_type_id,
            sub_packets=sub_packets,
        )


def get(data, num):
    string = "".join(islice(data, num))
    if not string:
        raise StopIteration()
    return string


def get_bin(data, num):
    string = get(data, num)
    return int(string, 2)


def parse_packets(data) -> Packet:
    data = iter(data)
    version = get_bin(data, 3)
    type_id = get_bin(data, 3)
    if type_id == 4:
        return LiteralPacket.from_stream(version, type_id, data)
    return OperatorPacket.from_stream(version, type_id, data)


class Visitor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def visit_operator(self, packet: OperatorPacket):
        ...

    @abc.abstractmethod
    def visit_literal(self, packet: OperatorPacket):
        ...


class VersionSumVisitor(Visitor):
    def __init__(self):
        self.sum = 0

    def visit_operator(self, packet: OperatorPacket):
        self.sum += packet.version

    def visit_literal(self, packet: LiteralPacket):
        self.sum += packet.version


def traverse(packet: Packet, visitor: Visitor):
    if isinstance(packet, LiteralPacket):
        visitor.visit_literal(packet)
    elif isinstance(packet, OperatorPacket):
        for sub_packet in packet.sub_packets:
            traverse(sub_packet, visitor)
        visitor.visit_operator(packet)


class EvaluatorVisitor(Visitor):
    def __init__(self):
        self.values = []

    def visit_literal(self, packet: LiteralPacket):
        self.values.append(packet.number)

    def visit_operator(self, packet: OperatorPacket):
        sub_packet_values = [self.values.pop() for _ in packet.sub_packets][::-1]
        if packet.type_id == 0:
            value = sum(sub_packet_values)
        elif packet.type_id == 1:
            value = math.prod(sub_packet_values)
        elif packet.type_id == 2:
            value = min(sub_packet_values)
        elif packet.type_id == 3:
            value = max(sub_packet_values)
        elif packet.type_id == 5:
            value = int(sub_packet_values[0] > sub_packet_values[1])
        elif packet.type_id == 6:
            value = int(sub_packet_values[0] < sub_packet_values[1])
        elif packet.type_id == 7:
            value = int(sub_packet_values[0] == sub_packet_values[1])
        self.values.append(value)


def part1():
    data = decode(load_input()[0])
    packet = parse_packets(data)
    visitor = VersionSumVisitor()
    traverse(packet, visitor)
    return visitor.sum


def evaluate(hexadecimal_chars):
    data = decode(hexadecimal_chars)
    packet = parse_packets(data)
    visitor = EvaluatorVisitor()
    traverse(packet, visitor)
    return visitor.values[0]


def part2():
    return evaluate(load_input()[0])


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
