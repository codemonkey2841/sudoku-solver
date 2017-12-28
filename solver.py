#!/usr/bin/env python3

from collections import Counter
from copy import deepcopy


class ViolationException(Exception):
    pass


class InvalidDimensionsException(Exception):
    pass


class Puzzle(object):

    def __init__(self, puzzle, i=0):
        if len(puzzle) != len(puzzle[0]):
            raise InvalidDimensionsException
        self.size = len(puzzle)
        self.puzzle = puzzle
        self.build_possibles()
        self.check_violations()
        self.i = i

    def assign(self, x, y, d):
        if d in self.get_existing(x, y):
            raise ViolationException
        self.puzzle[x][y] = d
        self.discard(x, y, d)

    def build_possibles(self):
        domain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for i in range(self.size):
            for j in range(self.size):
                item = self.puzzle[i][j]
                if type(item) != set and item == '.':
                    existing = self.get_existing(i, j)
                    self.puzzle[i][j] = domain - existing

    def check_violations(self):
        for i in range(self.size):
            # Check rows for duplicates
            temp = []
            for item in self.row(i):
                if type(item) != set:
                    temp.append(item)
            row = Counter(temp)
            for key, val in row.items():
                if val > 1:
                    raise ViolationException

            # Check columns for duplicates
            temp = []
            for item in self.column(i):
                if type(item) != set:
                    temp.append(item)
            col = Counter(temp)
            for key, val in col.items():
                if val > 1:
                    raise ViolationException

            # Check squares for duplicates
            for j in range(0, self.size, 3):
                temp = []
                for item in self.square(i, j):
                    if type(item) != set:
                        temp.append(item)
                square = Counter(temp)
                for key, val in square.items():
                    if val > 1:
                        raise ViolationException

    def column(self, y):
        return [self.puzzle[x][y] for x in range(self.size)]

    def discard(self, x, y, d):
        for item in self.row(x):
            if type(item) == set:
                item.discard(d)
                if len(item) == 0:
                    raise ViolationException

        for item in self.column(y):
            if type(item) == set:
                item.discard(d)
                if len(item) == 0:
                    raise ViolationException

        for item in self.square(x, y):
            if type(item) == set:
                item.discard(d)
                if len(item) == 0:
                    raise ViolationException

    def get_existing(self, x, y):
        existing = set()

        for item in self.row(x):
            if type(item) != set:
                existing.add(item)

        for item in self.column(y):
            if type(item) != set:
                existing.add(item)

        for item in self.square(x, y):
            if type(item) != set:
                existing.add(item)

        return existing

    def reduce(self):
        changes = 0
        while changes != self.unsolved_cells:
            changes = self.unsolved_cells
            for x in range(self.size):
                for y in range(self.size):
                    item = self.puzzle[x][y]
                    if type(item) == set and len(item) == 1:
                        self.assign(x, y, item.pop())

    def row(self, x):
        return self.puzzle[x]

    def solve(self):
        changes = 0
        while changes != self.unsolved_cells:
            changes = self.unsolved_cells
            self.solve_unique()
            self.reduce()

        if self.unsolved_cells == 0:
            return

        # backtrack
        for x in range(self.size):
            for y in range(self.size):
                item = deepcopy(self.puzzle[x][y])
                if type(item) == set:
                    for i in item:
                        temp = deepcopy(self.puzzle)
                        try:
                            p = Puzzle(temp, self.i+1)
                            p.assign(x, y, i)
                            p.solve()
                        except ViolationException:
                            # TODO something?
                            continue
                        if p.unsolved_cells == 0:
                            self.check_violations()
                            self.puzzle = p.puzzle
                            return
                    raise ViolationException

    def solve_unique(self):
        for x in range(self.size):
            for y in range(self.size):
                item = self.puzzle[x][y]
                if type(item) == set:
                    for i in item:
                        # check row for i in sets
                        check = True
                        for j in range(9):
                            if j != y:
                                a = self.row(x)[j]
                                if type(a) == set and i in a:
                                    check = False
                        if check:
                            self.assign(x, y, i)
                            break

                        # check column for i in sets
                        check = True
                        for j in range(9):
                            if j != y:
                                a = self.column(y)[j]
                                if type(a) == set and i in a:
                                    check = False
                        if check:
                            self.assign(x, y, i)
                            break

                        # check square for i in sets
                        check = True
                        for j in range(9):
                            if j != y:
                                a = self.square(x, y)[j]
                                if type(a) == set and i in a:
                                    check = False
                        if check:
                            self.assign(x, y, i)
                            break

    def square(self, x, y):
        xmin = x // 3 * 3
        ymin = y // 3 * 3
        square = []
        for i in range(xmin, xmin + 3):
            for j in range(ymin, ymin + 3):
                square.append(self.puzzle[i][j])
        return square

    @property
    def unsolved_cells(self):
        counter = 0
        for row in self.puzzle:
            for item in row:
                if type(item) == set:
                    counter += 1
        return counter

    def __repr__(self):
        self.__str__()

    def __str__(self):
        output = ''
        counter = 0
        for row in self.puzzle:
            scounter = 0
            for item in row:
                output += str(item)
                scounter += 1
                if scounter % 9 == 0:
                    output += '\n'
                elif scounter % 3 == 0:
                    output += '|'
            counter += 1
            if counter % 3 == 0 and counter < self.size:
                output += '---+---+---\n'
        return output


def main():
    puzzle = []
    for i in range(9):
        row = list(input())
        for i in range(9):
            if row[i] != '.':
                row[i] = int(row[i])
        puzzle.append(row)
    p = Puzzle(puzzle)
    p.solve()
    print(p)


if __name__ == '__main__':
    main()
