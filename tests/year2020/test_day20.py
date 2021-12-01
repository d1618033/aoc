from textwrap import dedent

from aoc.year2020.day20 import (
    fliph,
    flipv,
    get_full_image,
    get_full_image_no_borders,
    get_match,
    get_rotation,
    load_data,
    part1,
    part2,
    rotate,
)


def test_part1():
    assert part1() == 20899048083289


def test_part2():
    assert part2() == 273


def test_rotate():
    image = [
        ["a", "b", "c"],
        ["d", "e", "f"],
        ["g", "h", "i"],
    ]
    assert rotate(image) == [
        ["g", "d", "a"],
        ["h", "e", "b"],
        ["i", "f", "c"],
    ]


def test_fliph():
    image = [
        ["a", "b", "c"],
        ["d", "e", "f"],
        ["g", "h", "i"],
    ]
    assert fliph(image) == [
        ["c", "b", "a"],
        ["f", "e", "d"],
        ["i", "h", "g"],
    ]


def test_flipv():
    image = [
        ["a", "b", "c"],
        ["d", "e", "f"],
        ["g", "h", "i"],
    ]
    assert flipv(image) == [
        ["g", "h", "i"],
        ["d", "e", "f"],
        ["a", "b", "c"],
    ]


def test_get_rotation():
    assert get_rotation("right", "left") == 0
    assert get_rotation("right", "right") == 2
    assert get_rotation("right", "top") == 3
    assert get_rotation("right", "bottom") == 1
    assert get_rotation("left", "left") == 2
    assert get_rotation("left", "right") == 0
    assert get_rotation("left", "top") == 1
    assert get_rotation("left", "bottom") == 3


def test_get_full_image():
    image = flipv(get_full_image())
    print("\n".join("".join(row) for row in image))
    expected_str = dedent(
        """
    #...##.#....###..####.#.#####.
    ..#.#..#.####...#.#..#..######
    .###....#...#....#....#.......
    ###.##.##..#.#.#..########....
    .###.#######...#.#######.#..#.
    .##.#....###.##.###..#...#.##.
    #...##########.#...##.#####.##
    .....#..###...##..#...#.###...
    #.####...###..#.......#.......
    #.##...##...##.#..#...#.###...
    #.##...##...##.#..#...#.###...
    ##..#.##....#..###.###.##....#
    ##.####....#.####.#...#.###..#
    ####.#.#.....#.########.#..###
    .#.####......##..##..######.##
    .##..##.#.....#...###.#.#.#...
    ....#..#.##.#.#.##.##.###.###.
    ..#.#......#.##.#..##.###.##..
    ####.#.....#..#.##...######...
    ...#.#.#.####.##.#...##...####
    ...#.#.#.####.##.#...##...####
    ..#.#.###...##.##.###..#.##..#
    ..####.#####.#...##..#.#..#.##
    #..#.#..#....#.#.#...####.###.
    .#..####.##..#.#.#.#####.###..
    .#####..#######...#..##....##.
    ##.##..#....#...#....####...#.
    #.#.###....##..##....####.##.#
    #...###.....##...#.....#..####
    ..#.#....###.#.#.......##.....
    """
    ).strip()

    expected = [
        list(row.strip()) for row in expected_str.strip().splitlines() if row.strip()
    ]
    assert len(expected) == len(image)
    for i, (actual_row, expected_row) in enumerate(zip(image, expected)):
        assert "".join(actual_row) == "".join(expected_row), f"i: {i}"


def test_get_full_image_no_borders():
    image = flipv(get_full_image_no_borders())
    print("\n".join("".join(row) for row in image))
    expected_str = dedent(
        """
    .#.#..#.##...#.##..#####
    ###....#.#....#..#......
    ##.##.###.#.#..######...
    ###.#####...#.#####.#..#
    ##.#....#.##.####...#.##
    ...########.#....#####.#
    ....#..#...##..#.#.###..
    .####...#..#.....#......
    #..#.##..#..###.#.##....
    #.####..#.####.#.#.###..
    ###.#.#...#.######.#..##
    #.####....##..########.#
    ##..##.#...#...#.#.#.#..
    ...#..#..#.#.##..###.###
    .#.#....#.##.#...###.##.
    ###.#...#..#.##.######..
    .#.#.###.##.##.#..#.##..
    .####.###.#...###.#..#.#
    ..#.#..#..#.#.#.####.###
    #..####...#.#.#.###.###.
    #####..#####...###....##
    #.##..#..#...#..####...#
    .#.###..##..##..####.##.
    ...###...##...#...#..###
    """
    ).strip()

    expected = [
        list(row.strip()) for row in expected_str.strip().splitlines() if row.strip()
    ]
    assert len(expected) == len(image)
    for i, (actual_row, expected_row) in enumerate(zip(image, expected)):
        assert "".join(actual_row) == "".join(expected_row), f"i: {i}"


def test_get_match():
    image_parts = {image_part.id: image_part for image_part in load_data()}
    assert get_match(image_parts[2311], image_parts[1951])
    assert get_match(image_parts[2311], image_parts[3079])
    assert get_match(image_parts[2311], image_parts[1427])
    assert not get_match(image_parts[2311], image_parts[1489])
