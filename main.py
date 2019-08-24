"""Main Script

Command line interface for the Game of life.
"""

import sys
import argparse
from math import inf

from gol import GameOfLife


def parse_args():
    """Parse and return the necessary arguments."""

    parser = argparse.ArgumentParser(
        prog='A Random Game of Life',
        description="Conway's Game of Life in console")
    parser.add_argument('-p', '--pattern',
                        help='initial pattern name',
                        dest='pattern_file_name', default='glider')
    parser.add_argument('-r', '--random-rate',
                        help='generation of random pattern with some rate',
                        type=float, default=0.0)
    parser.add_argument('-t', '--time-step',
                        help='time between each step (seconds)',
                        type=float,
                        default=0.2)
    parser.add_argument('-m', '--max-gen',
                        help='maximum number of generation to execute',
                        type=int, default=inf)
    parser.add_argument('-i', '--inspect',
                        help='pause between each step',
                        action='store_true')
    parser.add_argument('-s', '--search',
                        help="search a pattern in 'patterns/'",
                        default='')
    parser.add_argument('--square-size',
                        help='size of the representation square',
                        type=int, default=5)
    parser.add_argument('--console-display',
                        help='console representation',
                        action='store_true')
    parser.add_argument('--alive-node-repr',
                        help='representation of an alive cell (one char)',
                        default='O')
    parser.add_argument('--dead-node-repr',
                        help='representation of a dead cell (one char)',
                        default='.')

    return vars(parser.parse_args(sys.argv[1:]))


if __name__ == '__main__':
    gol = GameOfLife(parse_args())
    gol.start()
