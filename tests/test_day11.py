from textwrap import dedent

from aoc.day11 import parse_data, part1, part2, run_game_of_life_step


def test_game_of_line_single_step():
    board = parse_data()
    expected_strings = """
        #.##.##.##
        #######.##
        #.#.#..#..
        ####.##.##
        #.##.##.##
        #.#####.##
        ..#.#.....
        ##########
        #.######.#
        #.#####.##
        ---
        #.LL.L#.##
        #LLLLLL.L#
        L.L.L..L..
        #LLL.LL.L#
        #.LL.LL.LL
        #.LLLL#.##
        ..L.L.....
        #LLLLLLLL#
        #.LLLLLL.L
        #.#LLLL.##
        ---
        #.##.L#.##
        #L###LL.L#
        L.#.#..#..
        #L##.##.L#
        #.##.LL.LL
        #.###L#.##
        ..#.#.....
        #L######L#
        #.LL###L.L
        #.#L###.##
        ---
        #.#L.L#.##
        #LLL#LL.L#
        L.L.L..#..
        #LLL.##.L#
        #.LL.LL.LL
        #.LL#L#.##
        ..L.L.....
        #L#LLLL#L#
        #.LLLLLL.L
        #.#L#L#.##
        ---
        #.#L.L#.##
        #LLL#LL.L#
        L.#.L..#..
        #L##.##.L#
        #.#L.LL.LL
        #.#L#L#.##
        ..L.L.....
        #L#L##L#L#
        #.LLLLLL.L
        #.#L#L#.##
        ---
        #.#L.L#.##
        #LLL#LL.L#
        L.#.L..#..
        #L##.##.L#
        #.#L.LL.LL
        #.#L#L#.##
        ..L.L.....
        #L#L##L#L#
        #.LLLLLL.L
        #.#L#L#.##
    """.split(
        "---"
    )
    for expected_str in expected_strings:
        run_game_of_life_step(board)
        assert_board_equal(board, expected_str.replace(" ", ""))


def assert_board_equal(board, expected_str):
    expected = dedent(expected_str).strip()
    assert board == expected


def test_part1():
    assert part1() == 37


def test_part2():
    assert part2() == 26
