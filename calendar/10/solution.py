from statistics import median

from helpers import open_file


class BracketChecker:
    BRACKET_MAP = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>',
    }

    def __call__(self, line):
        self.bracket_stack = []
        for bracket in line.strip():
            try:
                self.bracket_stack.append(self.BRACKET_MAP[bracket])
            except KeyError:
                last_item = self.bracket_stack.pop(-1)
                if last_item != bracket:
                    return bracket

bracket_checker = BracketChecker()


def get_error_score(line):
    return {
        None: 0,
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }[bracket_checker(line)]


def get_incomplete_score(line):
    bracket_points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }
    if bracket_checker(line)is None:
        score = 0
        for bracket in reversed(bracket_checker.bracket_stack):
            score = score * 5 + bracket_points[bracket]
        return score


def solve_pt1(f):
    return sum(map(lambda line: get_error_score(line), f.readlines()))


def solve_pt2(f):
    scores = map(lambda line: get_incomplete_score(line), f.readlines())
    return median(filter(lambda x: x is not None, scores))


assert solve_pt1(open_file("example.txt")) == 26397
assert solve_pt1(open_file("input.txt")) == 316851

assert solve_pt2(open_file("example.txt")) == 288957
assert solve_pt2(open_file("input.txt")) == 2182912364
