from helpers import open_file

from collections import Counter
from itertools import product
from typing import Generator, NamedTuple, IO, Type, TypeVar


_T = TypeVar("_T")


def _yield_range(start: int, end: int) -> Generator[int, None, None]:
    step = 1 if start <= end else -1
    yield from range(start, end + 1 * step, step)


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_string(cls: _T, s: str) -> _T:
        return cls(*(int(p) for p in s.split(',')))


class Line(NamedTuple):
    start: Point
    end: Point

    def yield_xs(self) -> Generator[int, None, None]:
        yield from _yield_range(self.start.x, self.end.x)

    def yield_ys(self) -> Generator[int, None, None]:
        yield from _yield_range(self.start.y, self.end.y)


class DiagonalLine(Line):
    def yield_points(self) -> Generator[Point, None, None]:
        for start, end in zip(self.yield_xs(), self.yield_ys()):
            yield Point(start, end)


class StraightLine(Line):
    def yield_points(self) -> Generator[Point, None, None]:
        for start, end in product(self.yield_xs(), self.yield_ys()):
            yield Point(start, end)


class LineFactory:
    def get_line(s: str) -> Type[Line]:
        start, end = map(lambda p: Point.from_string(p), s.split(" -> "))
        if start.x != end.x and start.y != end.y:
            return DiagonalLine(start, end)
        else:
            return StraightLine(start, end)


def _yield_lines(
        file: IO, ignore_diagonals=True
) -> Generator[Type[Line], None, None]:
    for line in file.read().splitlines():
        line = LineFactory.get_line(line)
        if not ignore_diagonals or not isinstance(line, DiagonalLine):
            yield line


def solve(f, ignore_diagonals=True) -> int:
    lines = _yield_lines(f, ignore_diagonals=ignore_diagonals)
    c = Counter(p for l in lines for p in l.yield_points())
    return len([v for v in c.values() if v > 1])


assert solve(open_file("example.txt")) == 5
assert solve(open_file("input.txt")) == 6461

assert solve(open_file("example.txt"), False) == 12
assert solve(open_file("input.txt"), False) == 18065