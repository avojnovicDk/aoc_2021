import os, sys

open_file = lambda filename: open(os.path.join(sys.path[0], filename), "r")


def to_decimal(binary_str):
    decimal = 0
    for i, bit in enumerate(reversed(binary_str)):
        if bit == '1':
            decimal += 2 ** i
    return decimal