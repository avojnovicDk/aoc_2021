from helpers import open_file


def solve_pt1(f):
    counter = 0
    prev = int(f.readline())
    for curr in f.readlines():
        curr = int(curr)
        if curr > prev:
            counter += 1

        prev = curr
    return counter


def solve_pt2(f):
    counter = 0
    win_diffs = [int(f.readline()) for _ in range(3)]

    for curr in f.readlines():
        curr = int(curr)
        if curr > win_diffs.pop(0):
            counter += 1
        win_diffs.append(curr)
    return counter


assert solve_pt1(open_file("example.txt")) == 7
assert solve_pt1(open_file("input.txt")) == 1564

assert solve_pt2(open_file("example.txt")) == 5
assert solve_pt2(open_file("input.txt")) == 1611
