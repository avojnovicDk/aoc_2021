from collections import defaultdict

from helpers import open_file


def solve_pt1(f):
    movement = defaultdict(int)
    for line in f.readlines():
        cmd, steps = line.split()
        movement[cmd] += int(steps)
    return movement["forward"] * (movement["down"] - movement["up"])


def solve_pt2(f):
    aim, horizontal, depth = 0, 0, 0
    for line in f.readlines():
        cmd, steps = line.split()
        steps = int(steps)
        if cmd == "forward":
            horizontal += steps
            depth += (aim * steps)
        elif cmd == "down":
            aim += steps
        elif cmd == "up":
            aim -= steps
    return horizontal * depth


assert solve_pt1(open_file("example.txt")) == 150
assert solve_pt1(open_file("input.txt")) == 1636725

assert solve_pt2(open_file("example.txt")) == 900
assert solve_pt2(open_file("input.txt")) == 1872757425