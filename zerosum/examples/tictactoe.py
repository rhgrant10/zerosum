# -*- coding: utf-8 -*-
import copy
import itertools
import collections

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
        yield from itertools.chain(self.rows, self.columns, self.diagonals)

    @property
    def blanks(self):
        for r in range(3):
            for c in range(3):
                if self.squares[r][c] == BLANK:
                    yield r, c

    def make_move(self, move):
        row, col = move
        piece = self.squares[row][col]
        if piece != BLANK:
            raise ValueError('Square {!r} already contains {!r}'
                             .format(move, piece))
        after_move = copy.deepcopy(self.squares)
        after_move[row][col] = self.player
        switched = tuple(reversed(self.players))
        return self.__class__(squares=after_move, players=switched)

    def __str__(self):
        rows = (' | '.join(row) for row in self.rows)
        return ' {}'.format('\n-----------\n '.join(rows))


class Evaluator(zerosum.base.Evaluator):
    def get_available_moves(self, board):
        return list(board.blanks)

    def get_winner(self, board):
        for line in board.lines:
            uniques = tuple(set(line))
            if len(uniques) == 1 and BLANK not in uniques:
                return uniques[0]


class TerminalEvaluator(Evaluator):
    prize = 10

    def __init__(self, prize=None):
        super().__init__()
        self.prize = prize or self.prize

    def get_score(self, board, depth=0):
        winner = self.get_winner(board)
        if winner:
            color = 1 if winner == board.player else -1
            return color * (self.prize + depth)
        return 0


class SmartEvaluator(Evaluator):
    points = {0: 0, 1: .1, 2: 1, 3: 10}

    def __init__(self, points=None):
        self.points = points or self.points

    def get_score(self, board, depth=0):
        score = 0
        for line in board.lines:
            pieces = collections.Counter(line)
            if not pieces[board.opponent]:
                count = pieces[board.player]
                score += self.points[count] + depth
            elif not pieces[board.player]:
                count = pieces[board.opponent]
                score -= self.points[count] + depth
        return score
