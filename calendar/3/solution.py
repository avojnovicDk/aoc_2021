from itertools import groupby

from helpers import open_file, to_decimal


def _pick_group_by_bit_at_pos(group, pos, pick_majority):
    g1, g2 = [list(g[1]) for g in groupby(sorted(group), key=lambda x: x[pos])]
    return (
        (g1 if pick_majority else g2)
        if len(g1) > len(g2)
        else (g2 if pick_majority else g1)
    )


def _calc_rating(group, pick_majority):
    curr_pos = 0
    while (len(group) > 1):
        group = _pick_group_by_bit_at_pos(group, curr_pos, pick_majority)
        curr_pos += 1
    return group[0]


def solve_pt1(f):
    bit_counter = None
    for line in f.readlines():
        bit_counter = [
            (-1 if bit == '0' else 1) + (bit_counter[i] if bit_counter else 0)
            for i, bit in enumerate(line.strip())
        ]

    gamma_rate, epsilon_rate = 0, 0
    for position, bit_count in enumerate(reversed(bit_counter)):
        decimal_part = 2 ** position
        if bit_count > 0:
            gamma_rate += decimal_part
        else:
            epsilon_rate += decimal_part
    return gamma_rate * epsilon_rate


def solve_pt2(f):
    group = f.read().splitlines()
    oxy_rating = to_decimal(_calc_rating(group, True))
    co2_rating = to_decimal(_calc_rating(group, False))
    return oxy_rating * co2_rating


assert solve_pt1(open_file("example.txt")) == 198
assert solve_pt1(open_file("input.txt")) == 2640986

assert solve_pt2(open_file("example.txt")) == 230
assert solve_pt2(open_file("input.txt")) == 6822109
