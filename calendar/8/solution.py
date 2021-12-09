from collections import Counter

from helpers import open_file


def solve_pt1(f):
    counter_1478 = 0
    for entry in f.readlines():
        _, outputs = entry.split('|')
        outputs_per_len = Counter(len(output) for output in outputs.split())
        counter_1478 += sum(outputs_per_len[i] for i in (2, 3, 4, 7))
    return counter_1478


def solve_pt2(f):
    total_value = 0
    for entry in f.readlines():
        signal_patterns, outputs = entry.split('|')
        outputs = outputs.split()
        signal_patterns = signal_patterns.split()
        pattern_map = dict()
        signal_patterns = sorted(signal_patterns, key=lambda p: len(p))
        cf, acf = signal_patterns[0], signal_patterns[1]
        bcdf = next(filter(lambda p: len(p) == 4, signal_patterns))
        ac, dg = '', ''
        for c, occur in Counter(s for p in signal_patterns for s in p).items():
            if occur == 9:
                pattern_map['f'] = c
            elif occur == 8:
                ac += c
            elif occur == 7:
                dg += c
            elif occur == 6:
                pattern_map['b'] = c
            elif occur == 4:
                pattern_map['e'] = c
        pattern_map['c'] = cf.replace(pattern_map['f'], '')
        pattern_map['a'] = ac.replace(pattern_map['c'], '')
        pattern_map['f'] = acf
        for c in ('a','c'):
            pattern_map['f'] = pattern_map['f'].replace(pattern_map[c], '')
        pattern_map['d'] = bcdf
        for c in ('b','c', 'f'):
            pattern_map['d'] = pattern_map['d'].replace(pattern_map[c], '')
        pattern_map['g'] = dg.replace(pattern_map['d'], '')
        pattern_map = {v: k for k, v in pattern_map.items()}
        digit_map = {
            'abcefg': 0,
            'cf': 1,
            'acdeg': 2,
            'acdfg': 3,
            'bcdf': 4,
            'abdfg': 5,
            'abdefg': 6,
            'acf': 7,
            'abcdefg': 8,
            'abcdfg': 9,
        }
        value = ''
        for output in outputs:
            decoded = ''.join(sorted(map(lambda x: pattern_map[x], output)))
            value += str(digit_map[decoded])
        total_value += int(value)
    return total_value


assert solve_pt1(open_file("example.txt")) == 26
assert solve_pt1(open_file("input.txt")) == 344

assert solve_pt2(open_file("example.txt")) == 61229
assert solve_pt2(open_file("input.txt")) == 1048410
