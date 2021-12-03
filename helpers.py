import os, sys

open_file = lambda filename: open(os.path.join(sys.path[0], filename), "r")
