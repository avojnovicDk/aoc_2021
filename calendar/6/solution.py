from helpers import open_file

from collections import Counter


def solve(f, days_count):
    lanternfish = Counter((int(fish)) for fish in f.readline().split(','))

    for _ in range(days_count):
        lanternfish = Counter(
            {timer - 1: count for timer, count in lanternfish.items()}
        )
        lanternfish[8] = lanternfish.pop(-1, 0)
        lanternfish[6] += lanternfish[8]
    return sum(lanternfish.values())


assert solve(open_file("example.txt"), 80) == 5934
assert solve(open_file("input.txt"), 80) == 386536

assert solve(open_file("example.txt"), 256) == 26984457539
assert solve(open_file("input.txt"), 256) == 1732821262171
