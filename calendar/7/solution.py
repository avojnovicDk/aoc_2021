from statistics import median

from helpers import open_file


def solve_pt1(f):
    positions = [int(p) for p in f.readline().split(',')]
    return sum(abs(p - int(median(positions))) for p in positions)


def solve_pt2(f):
    positions = [int(p) for p in f.readline().split(',')]
    mean = sum(positions) / len(positions)
    calc_fuel = lambda x: sum(
        abs(x - p) * (abs(x - p) + 1) /2 for p in positions
    )
    return min(calc_fuel(int(mean - 0.5)), calc_fuel(int(mean + 0.5)))


assert solve_pt1(open_file("example.txt")) == 37
assert solve_pt1(open_file("input.txt")) == 340056

assert solve_pt2(open_file("example.txt")) == 168
assert solve_pt2(open_file("input.txt")) == 96592275
