from collections import defaultdict, Counter

from helpers import open_file


class CaveMap:
    def __init__(self, edges, is_invalid=None):
        self.edges = edges
        if is_invalid is None:
            self.is_invalid = self._is_small_cave_revisit
        else:
            self.is_invalid = is_invalid

    @classmethod
    def from_file(cls, f, *args, **kwargs):
        edges = defaultdict(list)
        for line in f.readlines():
            n1, n2 = line.strip().split('-')
            edges[n1].append(n2)
            edges[n2].append(n1)
        return cls(edges, *args, **kwargs)

    @staticmethod
    def _has_revisited_small_cave(path):
        return Counter(filter(lambda n: n.islower(), path)).most_common(1)[0][1] == 2

    @staticmethod
    def _is_small_cave_revisit(path, node):
        return node.islower() and node in path

    def _find_paths(self, path):
        for node in self.edges[path[-1]]:
            if node == "start":
                continue
            if self.is_invalid(path, node):
                continue
            if node == "end":
                yield path + [node]
            else:
                yield from self._find_paths(path + [node])

    @property
    def paths(self):
        return list(self._find_paths(["start"]))


def solve_pt1(f):
    return len(CaveMap.from_file(f).paths)


def solve_pt2(f):
    is_invalid = lambda path, node: (
        CaveMap._has_revisited_small_cave(path)
        and CaveMap._is_small_cave_revisit(path, node)
    )
    cm = CaveMap.from_file(f, is_invalid=is_invalid)
    return len(cm.paths)


assert solve_pt1(open_file("example_1.txt")) == 10
assert solve_pt1(open_file("example_2.txt")) == 19
assert solve_pt1(open_file("example_3.txt")) == 226
assert solve_pt1(open_file("input.txt")) == 5212

assert solve_pt2(open_file("example_1.txt")) == 36
assert solve_pt2(open_file("example_2.txt")) == 103
assert solve_pt2(open_file("example_3.txt")) == 3509
assert solve_pt2(open_file("input.txt")) == 134862
