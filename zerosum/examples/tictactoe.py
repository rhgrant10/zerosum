# -*- coding: utf-8 -*-
from copy import deepcopy
from itertools import chain

import zerosum


X, O = 'X', 'O'
BLANK = ' '


class Board(zerosum.base.Board):
    #: An empty board
    EMPTY = [
        [BLANK, BLANK, BLANK],
        [BLANK, BLANK, BLANK],
        [BLANK, BLANK, BLANK],
    ]

    def __init__(self, players=None, squares=None):
        self.players = players or (X, O)
        self.squares = squares or self.EMPTY.copy()

    @property
    def player(self):
        return self.players[0]

    @property
    def opponent(self):
        return self.players[1]

    @property
    def columns(self):
        yield from zip(*self.squares)

    @property
    def rows(self):
        yield from self.squares

    @property
    def diagonals(self):
        yield self.squares[0][0], self.squares[1][1], self.squares[2][2]
        yield self.squares[0][2], self.squares[1][1], self.squares[2][0]

    @property
    def lines(self):
        yield from chain(self.rows, self.columns, self.diagonals)
    
    @property
    def blanks(self):
        for r in range(3):
            for c in range(3):
                if self.squares[r][c] == BLANK:
                    yield r, c

    def get_available_moves(self):
        return list(self.blanks)

    def get_winner(self):
        for line in self.lines:
            uniques = tuple(set(line))
            if len(uniques) == 1 and BLANK not in uniques:
                return uniques[0]

    def make_move(self, move):
        row, col = move
        piece = self.squares[row][col]
        if piece != BLANK:
            raise ValueError('Square {!r} already contains {!r}'
                             .format(move, piece))
        after_move = deepcopy(self.squares)
        after_move[row][col] = self.player
        switched = tuple(reversed(self.players))
        return self.__class__(squares=after_move, players=switched)

    def __str__(self):
        rows = (' | '.join(row) for row in self.rows)
        return ' {}'.format('\n-----------\n '.join(rows))


class Evaluator(zerosum.base.Evaluator):
    def __init__(self, prize=10):
        self.prize = prize

    def score(self, board, depth=0):
        outcome = board.outcome
        if outcome == board.player:
            score = self.prize + depth
        elif outcome == board.opponent:
            score = -self.prize - depth
        else:
            score = 0
        return score
