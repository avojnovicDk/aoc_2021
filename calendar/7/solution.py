from statistics import median

from helpers import open_file


def solve_pt1(f):
    positions = [int(p) for p in f.readline().split(',')]
    return sum(abs(p - int(median(positions))) for p in positions)


def _get_min_fuel_cost(prev_fuel_cost, positions_to_check, calc_fuel_cost):
    for position in positions_to_check:
        fuel_cost = calc_fuel_cost(position)
        if fuel_cost > prev_fuel_cost:
            # solution has 1 local minimum, so when we see it
            # increase, we know that answer is prev iter
            return prev_fuel_cost
        prev_fuel_cost = fuel_cost


def solve_pt2(f):
    positions = [int(p) for p in f.readline().split(',')]
    calc_fuel_cost = lambda x: sum(
        [sum(range(abs(x - p) + 1)) for p in positions]
    )
    median_position = int(median(positions))
    median_fuel_cost = calc_fuel_cost(median_position)
    prev_fuel_cost = calc_fuel_cost(median_position + 1)
    if median_fuel_cost > prev_fuel_cost:
        return _get_min_fuel_cost(
            prev_fuel_cost,
            range(median_position + 2, max(positions) + 1),
            calc_fuel_cost
        )
    else:
        return _get_min_fuel_cost(
            median_fuel_cost,
            range(median_position - 1, -1, -1),
            calc_fuel_cost
        )


assert solve_pt1(open_file("example.txt")) == 37
assert solve_pt1(open_file("input.txt")) == 340056

assert solve_pt2(open_file("example.txt")) == 168
assert solve_pt2(open_file("input.txt")) == 96592275
