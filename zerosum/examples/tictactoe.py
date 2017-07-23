# -*- coding: utf-8 -*-
import collections
import copy
import itertools
import re

import zerosum


__all__ = ['X', 'O', 'BLANK', 'Board', 'SimpleEvaluator', 'SmartEvaluator',
           'HumanPlayer', 'SimplePlayer', 'SmartPlayer', 'Game']

X, O, BLANK = 'XO '  # noqa


class Board(zerosum.base.Board):
    #: An empty board
    EMPTY = [
        [BLANK, BLANK, BLANK],
        [BLANK, BLANK, BLANK],
        [BLANK, BLANK, BLANK],
    ]

    def __init__(self, players=None, squares=None):
        """Create a new tic tac toe board, empty by default.

        :param list players: two player pieces ('X' and 'O') in order of play
        :param list squares: 3 lists of 3 peices that represent the board
        """
        self.players = players or (X, O)
        self.squares = squares or copy.deepcopy(self.EMPTY)

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
        """Make the given move on the board.

        :param tuple move: the move to make
        :return: a new board instance representing the resulting board
        :rtype: :class:`~zerosum.base.Board`
        """
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
        """Return all valid, available moves.

        :return: available moves
        :rtype: list
        """
        return list(self.blanks) if not self.get_winner() else []

    def get_winner(self):
        """Return the winning player if one exists.

        :return: the winner or ``None``
        :rtype: str
        """
        for line in self.lines:
            uniques = tuple(set(line))
            if len(uniques) == 1 and BLANK not in uniques:
                return uniques[0]

    def is_game_over(self):
        """Return true if the game is over.

        :return: whether the game is over
        :rtype: bool
        """
        return self.get_winner() or not self.get_available_moves()

    def __str__(self):
        rows = (' | '.join(row) for row in self.rows)
        return ' {}'.format('\n-----------\n '.join(rows))


class SimpleEvaluator(zerosum.base.Evaluator):

    def __init__(self, prize=10):
        """Create a simple board evaluator.

        Although it does consider depth, this evaluator scores only final game
        positions.

        :param float prize: the prize for a winning board
        """
        super().__init__()
        self.prize = prize

    def get_score(self, board, depth=0):
        """Return the score for the given board at the given depth.

        :param board: the board to score
        :type board: :class:`~zerosum.base.Board`
        :param int depth: the search depth at which this board was found
        :return: the score of the board
        :rtype: float
        """
        winner = board.get_winner()
        if winner:
            color = 1 if winner == board.player else -1
            return color * (self.prize + depth)
        return depth


class SmartEvaluator(zerosum.base.Evaluator):
    points = {0: 0, 1: 10, 2: 100, 3: 1000}

    def __init__(self, points=None):
        """Create a new smart board evaluator.

        This evaluator works by scoring the number of squares a player has on
        each line. A line with both players on it is worth nothing to either
        player.

        :param dict points: a map of points to award for each line
        """
        self.points = points or self.points

    def get_score(self, board, depth=0):
        """Return the score for the given board at the given depth.

        :param board: the board to score
        :type board: :class:`~zerosum.base.Board`
        :param int depth: the search depth at which this board was found
        :return: the score of the board
        :rtype: float
        """
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
    move_re = re.compile(r'''^(?P<row>[012]).*(?P<column>[012])$''')
    prompt = "What's your move? ('q' to quit) "

    def __init__(self, name, move_re=None, prompt=None):
        """Create a new human tic tac toe player.

        :param str name: the player's name
        :param str move_re: a regular expression that matches a valid move
        :param str prompt: the prompt text for a move
        """
        super().__init__(name=name)
        self.move_re = move_re or self.move_re
        self.prompt = prompt or self.prompt

    def get_input(self):
        """Get the player's move input.

        :return: the raw move input from the player
        :rtype: str
        """
        return input(self.prompt)

    def parse_move_input(self, move_input):
        """Convert the raw move into an actual move.

        :param str move_input: the raw move input from the user
        :return: the actual move as row and column
        :rtype: tuple
        """
        match = self.move_re.match(move_input)
        if match:
            row, column = match.group('row', 'column')
            return int(row), int(column)
        raise zerosum.exceptions.InvalidMove(player=self, move=move_input)

    def is_quit(self, move_input):
        """Return ``True`` if the move input represents "I quit."

        :param str move_input: the raw move input
        :return: whether the move input means that the player quits
        :rtype: bool
        """
        return move_input == 'q'


class AiPlayer(zerosum.base.AiPlayer):
    def __init__(self, evaluator, max_depth=None):
        solver = zerosum.solvers.AlphaBeta(evaluator=evaluator,
                                           max_depth=max_depth)
        super().__init__(solver=solver)

    def take_pre_turn(self, board):
        print('Thinking...')


class SimplePlayer(AiPlayer):
    """A player that uses the :class:`~SimpleEvaluator`."""

    def __init__(self, max_depth=None):
        """CReate a new ``SimplePlayer``.

        :param int max_depth: the maximum allowable solver depth
        """
        super().__init__(evaluator=SimpleEvaluator(), max_depth=max_depth)


class SmartPlayer(AiPlayer):
    """A player that uses the :class:`~SmartEvaluator`."""

    def __init__(self, max_depth=None):
        """CReate a new ``SmartPlayer``.

        :param int max_depth: the maximum allowable solver depth
        """
        super().__init__(evaluator=SmartEvaluator(), max_depth=max_depth)


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
