# -*- coding: utf-8 -*-
import copy
import itertools
import collections
import re

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
        try:
            row, col = move
        except (ValueError, TypeError):
            message = "Can't decompose {!r} into a row and a column"
            raise ValueError(message.format(move))

        piece = self.squares[row][col]
        if piece != BLANK:
            message = 'Square {!r} already contains {!r}'
            raise ValueError(message.format(move, piece))

        squares = copy.deepcopy(self.squares)
        squares[row][col] = self.player
        players = tuple(reversed(self.players))
        return self.__class__(squares=squares, players=players)

    def get_available_moves(self):
        return list(self.blanks) if not self.get_winner() else []

    def get_winner(self):
        for line in self.lines:
            uniques = tuple(set(line))
            if len(uniques) == 1 and BLANK not in uniques:
                return uniques[0]

    def is_game_over(self):
        return self.get_winner() or not self.get_available_moves()

    def __str__(self):
        rows = (' | '.join(row) for row in self.rows)
        return ' {}'.format('\n-----------\n '.join(rows))


class SimpleEvaluator(zerosum.base.Evaluator):
    prize = 10

    def __init__(self, prize=None):
        super().__init__()
        self.prize = prize or self.prize

    def get_score(self, board, depth=0):
        winner = board.get_winner()
        if winner:
            color = 1 if winner == board.player else -1
            return color * (self.prize + depth)
        return depth


class SmartEvaluator(zerosum.base.Evaluator):
    points = {0: 0, 1: 10, 2: 100, 3: 1000}

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


class HumanPlayer(zerosum.base.HumanPlayer):
    move_re = re.compile(r'''^(?P<row>[012]).+(?P<column>[012])$''')
    prompt = "What's your move? ('q' to quit) "

    def __init__(self, name, move_re=None, prompt=None):
        super().__init__(name=name)
        self.move_re = move_re or self.move_re
        self.prompt = prompt or self.prompt

    def get_input(self):
        return input(self.prompt)

    def parse_move_input(self, response):
        match = self.move_re.match(response)
        if match:
            row, column = match.group('row', 'column')
            return int(row), int(column)
        raise zerosum.exceptions.InvalidMove(player=self, move=response)

    def is_quit(self, move):
        return move == 'q'


class AiPlayer(zerosum.base.AiPlayer):
    def take_pre_turn(self, board):
        print('Thinking...')


class SimplePlayer(AiPlayer):
    def __init__(self, max_depth=None):
        evaluator = SimpleEvaluator()
        solver = zerosum.solvers.Minimax(evaluator=evaluator,
                                         max_depth=max_depth)
        super().__init__(solver=solver)


class SmartPlayer(AiPlayer):
    def __init__(self, max_depth=None):
        evaluator = SmartEvaluator()
        solver = zerosum.solvers.Minimax(evaluator=evaluator,
                                         max_depth=max_depth)
        super().__init__(solver=solver)


class Game(zerosum.base.Game):
    def intro_hook(self):
        header = '\n{0} {1} vs {2} {0}\n'
        banner = '~' * 10
        print(header.format(banner, *self.players.values()))
        print(self.board)

    def pre_turn_hook(self):
        print("{}, it's your turn.".format(self.player))

    def post_turn_hook(self):
        print(self.board)

    def player_quit_hook(self, e):
        print('Player {} quits!'.format(e.player))

    def invalid_move_hook(self, e):
        print('{!r} is an invalid move yo... try again.'.format(e.move))
