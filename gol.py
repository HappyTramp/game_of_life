"""Module that contain the GameOfLife class

The Game append on an infinite 2D grid,
each node of it can be either alive or dead.

A dead node become alive if he as 3 alive neighbors,
an alive node become dead if he as less than 2 or more than 3 neighbors,
else they stay in their current state.
"""

import re
import os
import sys
from time import sleep
from math import inf
from random import random
from itertools import product, count
from functools import reduce
from collections import namedtuple

from graphic import Graphic


class GameOfLife:
    """Class of Conway's Game of life"""

    NEIGHBORS_MOD = list(product([-1, 0, 1], repeat=2))
    SIZE = namedtuple('Size', 'w h')
    NODE = namedtuple('Node', 'x y')

    def __init__(self, kwargs):
        """Initialize the set of alive nodes with the selected options."""

        self.generation_counter = 0
        self.pattern_name = ''
        for key, value in kwargs.items():
            setattr(self, key, value)

        if kwargs['search'] != '':
            self._search_pattern(kwargs['search'])

        if self.random_rate != 0.0:
            self.size = self.SIZE(100, 100)
            self.alive_nodes = {
                self.NODE(x, y) for x in range(self.size.h)
                for y in range(self.size.w)
                if random() < self.random_rate}
        else:
            self.alive_nodes = {
                self.NODE(x, y) for x, row in enumerate(
                    self._generate_pattern_grid_from_file())
                for y, node in enumerate(row) if node}

    def _search_pattern(self, search):
        file_names = os.listdir('./patterns')
        match = sorted(
            filter(lambda n: re.match(r'.*' + re.escape(search) + r'.*', n),
                    map(lambda n: n[:-4], file_names)),
            key=lambda k: len(k)
        )
        for m in match:
            print(f'- {m}')
        sys.exit()

    def _generate_pattern_grid_from_file(self):
        """ Try to read the file with the pattern_name,
        and extract a grid of 1's and 0's from it.
        """

        with open(f'./patterns/{self.pattern_file_name}.rle', 'r') as pattern_file:
            for line in pattern_file:
                if line[0] == '#':
                    if line[1] == 'N':
                        self.pattern_name = line[3:-1]
                elif line[0] == 'x':
                    self.size = self.SIZE(*map(
                        int,
                        re.search(r'^x = (\d+), y = (\d+)', line).groups()))
                    break
            return [
                [
                    1 if n[-1] == 'o' else 0
                    for n in re.findall(r'(\d*[a-z])', line)
                    for _ in range(1 if len(n) == 1 else int(n[:-1]))]
                for line in pattern_file.read().replace('\n', '').split('$')]

    def start(self):
        """Iterate over generations and print them."""

        if self.console_display:
            while self.generation_counter <= self.max_gen:
                self._console_display()
                self.next_generation()

        else:
            graphic = Graphic(self)
            graphic.main_loop()

    def _console_display(self):
        print(f'Generation: {self.generation_counter}\n{self._to_string()}\n')
        input('Press Enter') if self.inspect else sleep(self.time_step)

    def next_generation(self):
        """Go to the next generation."""

        alive_nodes_cpy = self.alive_nodes.copy()
        for n_pos in self._nodes_to_check():
            # Get the number of alive neighbors
            # around a cell to apply the rules on it.
            alive_neighbors = reduce(
                lambda acc, p: acc + 1 if p in self.alive_nodes else acc,
                [
                    (x + n_pos.x, y + n_pos.y)
                    for x, y in self.NEIGHBORS_MOD if (x, y) != (0, 0)
                ], 0)

            if n_pos not in self.alive_nodes and alive_neighbors == 3:
                alive_nodes_cpy.add(n_pos)
            elif n_pos in self.alive_nodes and not 2 <= alive_neighbors <= 3:
                alive_nodes_cpy.remove(n_pos)

        self.alive_nodes = alive_nodes_cpy
        self.generation_counter += 1

    def _nodes_to_check(self):
        """Return all the node to check at some generation"""

        return {self.NODE(x + n_pos.x, y + n_pos.y)
             for x, y in self.NEIGHBORS_MOD
             for n_pos in self.alive_nodes}

    def _to_string(self):
        """Convert a grid of positions in a string.
        Use the range of self width and height
        and the size of the pattern
        """

        return '\n'.join(
            [''.join([
                (self.alive_node_repr
                 if (x, y) in self.alive_nodes else self.dead_node_repr)
                for y in range(-28, 32)])
             for x in range(-13, 17)])
