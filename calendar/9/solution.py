from helpers import open_file


def yield_neighbours(heightmap, row_id, col_id):
    neighbour_deltas = ((0, -1), (0, 1), (-1, 0), (1, 0))
    for i, j in neighbour_deltas:
        if row_id + i < 0 or col_id + j < 0:
            continue
        try:
            yield heightmap[row_id + i][col_id + j]
        except IndexError:
            pass


def solve_pt1(f):
    heightmap = []
    for line in f.readlines():
        heightmap.append(list(map(lambda x: int(x), line.strip())))
    row_len, col_len = len(line), len(heightmap)
    risk_sum = 0

    for i in range(col_len):
        for j in range(row_len):
            curr_height = heightmap[i][j]
            is_low_point = True
            for neighbour in yield_neighbours(heightmap, i, j):
                if curr_height >= neighbour:
                    is_low_point = False
                    break
            if is_low_point:
                risk_sum += curr_height + 1
    return risk_sum


def yield_not_highest_ids(heightmap, row_id, col_id):
    neighbour_deltas = ((0, -1), (0, 1), (-1, 0), (1, 0))
    for i, j in neighbour_deltas:
        if row_id + i < 0 or col_id + j < 0:
            continue
        try:
            if heightmap[row_id + i][col_id + j] != 9:
                yield (row_id + i, col_id + j)
        except IndexError:
            pass


def get_basin(curr_point, heightmap, basin_points):
    for n in yield_not_highest_ids(heightmap, *curr_point):
        if n not in basin_points:
            basin_points.add(n)
            get_basin(n, heightmap, basin_points)


def solve_pt2(f):
    heightmap = []
    for line in f.readlines():
        heightmap.append(list(map(lambda x: int(x), line.strip())))
    row_len, col_len = len(line), len(heightmap)
    sizes = []

    for i in range(col_len):
        for j in range(row_len):
            curr_height = heightmap[i][j]
            is_low_point = True
            for neighbour in yield_neighbours(heightmap, i, j):
                if curr_height >= neighbour:
                    is_low_point = False
                    break
            if is_low_point:
                basin_points = {(i, j)}
                get_basin((i, j), heightmap, basin_points)
                sizes.append(len(basin_points))

    size_mul = 1
    for size in sorted(sizes, reverse=True)[:3]:
        size_mul *= size
    return size_mul


assert solve_pt1(open_file("example.txt")) == 15
assert solve_pt1(open_file("input.txt")) == 588

assert solve_pt2(open_file("example.txt")) == 1134
assert solve_pt2(open_file("input.txt")) == 964712
