from collections import Counter, defaultdict
from dataclasses import dataclass, field
from math import prod
from textwrap import dedent
from typing import Optional, List, Set, Tuple, Dict

from more_itertools import flatten

from aoc.utils import load_input, StringEnum


@dataclass
class ImagePart:
    id: int
    data: List[List[str]]
    attached: Dict["SideEnum", "ImagePart"] = field(default_factory=dict)

    @property
    def top(self):
        return tuple(self.data[0])

    @property
    def bottom(self):
        return tuple(self.data[-1])

    @property
    def left(self):
        return tuple([row[0] for row in self.data])

    @property
    def right(self):
        return tuple([row[-1] for row in self.data])

    @property
    def sides(self):
        for side in SideEnum:
            yield side, getattr(self, side)


class SideEnum(StringEnum):
    left = "left"
    right = "right"
    top = "top"
    bottom = "bottom"


class Orientation:
    side: SideEnum
    flipped: bool


def load_data():
    chunks = load_input(delim="\n\n")
    image_parts = []
    for chunk in chunks:
        lines = chunk.splitlines()
        if not lines:
            continue
        id_line = int(lines[0].replace("Tile ", "").replace(":", ""))
        image_parts.append(ImagePart(id=id_line, data=[[col for col in row] for row in lines[1:]]))
    return image_parts


def part1():
    image_parts = load_data()

    all_sides = defaultdict(set)
    for image_part in image_parts:
        for side_name, side in image_part.sides:
            for is_flipped, flip in [
                (False, side),
                (True, tuple(reversed(side)))
            ]:
                all_sides[flip].add(image_part.id)
    matches = defaultdict(set)
    for side, image_parts in all_sides.items():
        if len(image_parts) == 2:
            a, b = image_parts
            matches[a].add(b)
            matches[b].add(a)
    corners = [
        image_part_id
        for image_part_id, matches in matches.items()
        if len(matches) == 2
    ]
    assert len(corners) == 4
    return prod(corners)


def rotate(image):
    num_columns = len(image)
    num_rows = len(image[0])
    return [
        list(reversed([
            image[j][i]
            for j in range(num_columns)
        ]))
        for i in range(num_rows)
    ]


def fliph(image):
    return [
        list(reversed(row))
        for row in image
    ]


def flipv(image):
    return list(reversed(image))


def flip_side(image, side):
    if side in ["left", "right"]:
        return flipv(image)
    else:
        return fliph(image)


def get_match(image, other_image):
    for side_name, side in image.sides:
        for other_side_name, other_side in other_image.sides:
            if side == other_side:
                return side_name, other_side_name, False
            elif list(reversed(side)) == list(other_side):
                return side_name, other_side_name, True


def get_rotation(side, other_side):
    """
        1
      ______
    0 |    |  2
      ------
        3
    """
    string_to_index = {
        "left": 0,
        "top": 1,
        "right": 2,
        "bottom": 3,
    }
    side_index = string_to_index[side]
    other_side_index = string_to_index[other_side]
    desired_index = {0: 2, 1: 3, 3: 1, 2: 0}[side_index]
    if desired_index < other_side_index:
        desired_index += 4
    return desired_index - other_side_index


def get_full_image():
    complement_side = {"left": "right", "right": "left", "top": "bottom", "bottom": "top"}

    image_parts = load_data()
    assert set(Counter(tuple(reversed(side)) if rev else tuple(side) for img in image_parts for _, side in img.sides for rev in [True, False]).values()) <= {1, 2}

    images_to_check = [image_parts[0]]
    images_already_checked = []

    while images_to_check:
        print(f"Images to check: {[im.id for im in images_to_check]}")
        image = images_to_check.pop()
        assert image not in images_already_checked
        for other_image in image_parts:
            if other_image.id == image.id:
                continue
            if other_image in image.attached.values():
                continue
            if match := get_match(image, other_image):
                side, other_side, should_flip = match
                for _ in range(get_rotation(side, other_side)):
                    other_image.data = rotate(other_image.data)
                side, other_side, should_flip = get_match(image, other_image)
                assert complement_side[side] == other_side
                if getattr(image, side) != getattr(other_image, other_side):
                    other_image.data = flip_side(other_image.data, other_side)
                assert getattr(image, side) == getattr(other_image, other_side)
                other_side = complement_side[side]
                if side in image.attached:
                    print(f"Image {image.id} already attached at side {side} to {image.attached[side].id}, can't attach now {other_image.id}")
                    continue
                image.attached[side] = other_image
                assert other_side not in other_image.attached, f"other {other_image.id} already attached at side {other_side} to {other_image.attached[other_side].id}"
                other_image.attached[other_side] = image
                if other_image not in images_to_check and other_image not in images_already_checked:
                    images_to_check.append(other_image)
        images_already_checked.append(image)



    for im in image_parts:
        for side, other_im in im.attached.items():
            assert getattr(im, side) == getattr(other_im, complement_side[side])

    corners = [
        im
        for im in image_parts
        if len(im.attached) == 2
    ]
    assert len(corners) == 4

    full_image_size = int(len(image_parts) ** 0.5)

    borders = [
        im
        for im in image_parts
        if len(im.attached) == 3
    ]
    assert len(borders) == (full_image_size - 2) * 4, len(borders)


    full_image: List[List[ImagePart]] = [[None for _ in range(full_image_size)] for _ in range(full_image_size)]
    for corner in corners:
        if set(corner.attached.keys()) == {"bottom", "right"}:
            full_image[0][0] = corner
        if set(corner.attached.keys()) == {"bottom", "left"}:
            full_image[0][-1] = corner
        if set(corner.attached.keys()) == {"top", "right"}:
            full_image[-1][0] = corner
        if set(corner.attached.keys()) == {"top", "left"}:
            full_image[-1][-1] = corner
    assert sum(im is not None for im in flatten(full_image)) == 4

    print([[im.id if im else None for im in row] for row in full_image])

    while (num_none := sum(im is None for im in flatten(full_image))) > 0:
        print(f"Num none: {num_none}")
        for i, row in enumerate(full_image):
            assert len(row) == full_image_size
            for j, image in enumerate(row):
                print(i, j, image is not None)
                if image is None:
                    continue
                assert isinstance(image, ImagePart)
                print(i, j, image.id, image.attached.keys())
                if left := image.attached.get("left"):
                    full_image[i][j-1] = left
                if right := image.attached.get("right"):
                    full_image[i][j + 1] = right
                if top := image.attached.get("top"):
                    full_image[i - 1][j] = top
                if bottom := image.attached.get("bottom"):
                    full_image[i + 1][j] = bottom
    assert sum(im is None for im in flatten(full_image)) == 0

    print([[im.id for im in row] for row in full_image])

    assert set(full_image[0][-1].attached.keys()) == {"left", "bottom"}
    assert set(full_image[0][0].attached.keys()) == {"bottom", "right"}
    assert full_image[0][0].attached["right"].id == full_image[0][1].id
    assert full_image[0][1].attached["right"].id == full_image[0][2].id

    assert full_image[0][2].left == full_image[0][1].right

    assert full_image[0][0].right == full_image[0][1].left
    assert full_image[1][0].top == full_image[0][0].bottom
    assert full_image[1][1].top == full_image[0][1].bottom
    assert full_image[1][1].left == full_image[1][0].right
    assert full_image[1][2].left == full_image[1][1].right
    assert full_image[2][2].left == full_image[2][1].right

    assert full_image[1][1].right == full_image[1][2].left, f"{full_image[1][1].right} == {full_image[1][2].left}"
    assert full_image[1][1].bottom == full_image[2][1].top

    full_image_concatenated = []
    for image_part_row in full_image:
        for i in range(len(image_part_row[0].data)):
            full_image_concatenated.append(
                sum([image_part.data[i] for image_part in image_part_row], [])
            )

    return full_image_concatenated


def get_full_image_no_borders():
    image = get_full_image()
    def is_not_border(j):
        return j % 10 not in [9, 0]
    return [
        [
            col
            for j, col in enumerate(row)
            if is_not_border(j)
        ]
        for i, row in enumerate(image)
        if is_not_border(i)
    ]


def print_image(image):
    print('\n'.join(''.join(row) for row in image))


def part2():
    image = get_full_image_no_borders()
    sea_monster = [list(row) for row in dedent("""
        __________________#_
        #____##____##____###
        _#__#__#__#__#__#___
    """).strip().splitlines()]
    assert len(set(len(row) for row in sea_monster)) == 1
    assert len(sea_monster) == 3

    def equal_to_sea_monster(i, j):
        part_of_image = [
            row[j:j+len(sea_monster[0])]
            for row in image[i:i+len(sea_monster)]
        ]
        assert len(part_of_image) == len(sea_monster)
        assert len(part_of_image[0]) == len(sea_monster[0]), f"{len(part_of_image[0])} == {len(sea_monster[0])}"
        for i, row in enumerate(part_of_image):
            for j, col in enumerate(row):
                if sea_monster[i][j] == '_':
                    part_of_image[i][j] = '_'
        print_image(part_of_image)
        print()
        return part_of_image == sea_monster


    def fill_in_sea_monster(i, j):
        part_of_image = [
            row[j:j+len(sea_monster[0])]
            for row in image[i:i+len(sea_monster)]
        ]
        assert len(part_of_image) == len(sea_monster)
        assert len(part_of_image[0]) == len(sea_monster[0]), f"{len(part_of_image[0])} == {len(sea_monster[0])}"
        for i_, row in enumerate(part_of_image):
            for j_, col in enumerate(row):
                if sea_monster[i_][j_] != '_':
                    image[i+i_][j+j_] = 'O'

    # image = rotate(image)
    # print_image(image)
    # fill_in_sea_monster(2, 2)
    # fill_in_sea_monster(len(image) - 8, 1)
    # print_image(image)
    def get_sea_monsters(image):
        monsters = []
        for i in range(len(image) - len(sea_monster)):
            for j in range(len(image[i]) - len(sea_monster[0])):
                if equal_to_sea_monster(i, j):
                    monsters.append((i, j))
        return monsters

    for _ in range(3):
        image = rotate(image)
        found = False
        if monsters := get_sea_monsters(image):
            found = True
        elif monsters := get_sea_monsters(flipv(image)):
            found = True
        elif monsters := get_sea_monsters(fliph(image)):
            found = True
        if found:
            for i, j in monsters:
                fill_in_sea_monster(i, j)
            break
    return len([element for element in flatten(image) if element == '#'])




def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
