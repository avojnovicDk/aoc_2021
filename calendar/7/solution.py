from statistics import median

from helpers import open_file


def solve_pt1(f):
    positions = [int(p) for p in f.readline().split(',')]
    return sum(abs(p - int(median(positions))) for p in positions)


def solve_pt2(f):
    positions = [int(p) for p in f.readline().split(',')]
    prev_fuel_cost = None
    for position in range(min(positions), max(positions) + 1):
        fuel_cost = sum([sum(range(abs(position - p) + 1)) for p in positions])
        if prev_fuel_cost and fuel_cost > prev_fuel_cost:
            # solution has 1 local minimum, so when we see it
            # increase, we know that answer is prev iter
            return prev_fuel_cost
        prev_fuel_cost = fuel_cost


assert solve_pt1(open_file("example.txt")) == 37
assert solve_pt1(open_file("input.txt")) == 340056

assert solve_pt2(open_file("example.txt")) == 168
assert solve_pt2(open_file("input.txt")) == 96592275
