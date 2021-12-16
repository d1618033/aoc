import pytest

from aoc.year2021.day16 import (
    LiteralPacket,
    OperatorPacket,
    decode,
    evaluate,
    parse_packets,
    part1,
    part2,
)


@pytest.mark.parametrize(
    "hexa,expected",
    [
        ("1", "0001"),
        ("A", "1010"),
        ("AB", "10101011"),
        ("D2FE28", "110100101111111000101000"),
        ("38006F45291200", "00111000000000000110111101000101001010010001001000000000"),
    ],
)
def test_decode(hexa, expected):
    assert "".join(decode(hexa)) == expected


def test_literal_packet():
    packet = parse_packets("110100101111111000101000")
    assert isinstance(packet, LiteralPacket)
    assert packet.version == 6
    assert packet.type_id == 4
    assert packet.number == 2021


def test_operator_packet_length_type_0():
    packet = parse_packets("00111000000000000110111101000101001010010001001000000000")
    assert isinstance(packet, OperatorPacket)
    assert packet.version == 1
    assert packet.type_id == 6
    assert packet.length_type_id == 0
    assert len(packet.sub_packets) == 2
    assert packet.sub_packets[0].number == 10
    assert packet.sub_packets[1].number == 20


def test_operator_packet_length_type_1():
    packet = parse_packets("11101110000000001101010000001100100000100011000001100000")
    assert isinstance(packet, OperatorPacket)
    assert packet.version == 7
    assert packet.type_id == 3
    assert packet.length_type_id == 1
    assert len(packet.sub_packets) == 3
    assert packet.sub_packets[0].number == 1
    assert packet.sub_packets[1].number == 2
    assert packet.sub_packets[2].number == 3


def test_part1():
    assert part1() == 16


@pytest.mark.input_file("example_2")
def test_part2():
    assert part2() == 3


@pytest.mark.parametrize(
    "hexa,expected",
    [
        ("C200B40A82", 3),
        ("04005AC33890", 54.0),
        ("880086C3E88112", 7.0),
        ("CE00C43D881120", 9.0),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    ],
)
def test_evaluate(hexa, expected):
    assert evaluate(hexa) == expected
