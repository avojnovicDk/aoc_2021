from itertools import product

from helpers import open_file


class OctopusFlash:
    def __init__(self, energy):
        self.energy = energy

    @property
    def col_len(self):
        return len(self.energy)

    @property
    def row_len(self):
        return len(self.energy[0])

    @property
    def flashes_count(self):
        return len([o for row in self.energy for o in row if o == 0])

    @property
    def has_all_flashed(self):
        return self.flashes_count == self.col_len * self.row_len

    @classmethod
    def from_file(cls, f):
        energy = []
        for line in f.readlines():
            energy.append(list(map(lambda o: int(o), line.strip())))
        return cls(energy)

    def _increase_energy(self, rows, cols):
        for i, j in product(rows, cols):
            if self.energy[i][j] is None:
                continue

            self.energy[i][j] += 1
            if self.energy[i][j] >= 10:
                self.energy[i][j] = None
                self._increase_energy(
                    range(max(i - 1, 0), min(i + 2, self.row_len)),
                    range(max(j - 1, 0), min(j + 2, self.col_len))
                )

    def _cleanup(self):
        for i, j in product(range(0, self.row_len), range(0, self.col_len)):
            if self.energy[i][j] is None:
                self.energy[i][j] = 0

    def __call__(self, *args, **kwargs):
        self._increase_energy(range(0, self.row_len), range(0, self.col_len))
        self._cleanup()


def solve_pt1(f):
    flashes_count = 0
    fo = OctopusFlash.from_file(f)
    for _ in range(100):
        fo()
        flashes_count += fo.flashes_count
    return flashes_count


def solve_pt2(f):
    steps_count = 0
    fo = OctopusFlash.from_file(f)
    while not fo.has_all_flashed:
        steps_count += 1
        fo()
    return steps_count


assert solve_pt1(open_file("example.txt")) == 1656
assert solve_pt1(open_file("input.txt")) == 1686

assert solve_pt2(open_file("example.txt")) == 195
assert solve_pt2(open_file("input.txt")) == 2182912364
