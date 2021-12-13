from collections import defaultdict, Counter

from helpers import open_file


def fold_x(sheet, x):
    return set((x - abs(s[0] - x), s[1]) for s in sheet if s[0] != x)


def fold_y(sheet, y):
    return set((s[0], y - abs(s[1] - y)) for s in sheet if s[1] != y)


def solve(f, only_first=False):
    sheet = set()
    for line in f.readlines():
        if line.isspace():
            continue
        if line.startswith('fold along y='):
            sheet = fold_y(sheet, int(line.split('=')[1]))
            if only_first:
                return sheet
        elif line.startswith('fold along x='):
            sheet = fold_x(sheet, int(line.split('=')[1]))
            if only_first:
                return sheet
        else:
            x, y = map(int, line.split(','))
            sheet.add((x,y))
    return sheet


def display(sheet):
    for row_id in range(max(c[1] for c in sheet) + 1):
        print(
            ''.join(
                '#' if (col_id, row_id) in sheet else '.'
                for col_id in range(max(c[0] for c in sheet) + 1)
            )
        )


assert len(solve(open_file("example.txt"), only_first=True)) == 17
assert len(solve(open_file("input.txt"), only_first=True)) == 621

display(solve(open_file("example.txt")))
display(solve(open_file("input.txt")))