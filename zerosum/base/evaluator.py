# -*- coding: utf-8 -*-
import abc


class Evaluator(metaclass=abc.ABCMeta):

    def evaluate(self, board):
        """Return an evaluation of a board.

        :param board: the board to evaluate
        :type board: `zerosum.base.board`
        :return: an evaluation of the board
        :rtype: `zerosum.base.evaluations.Evaluator`
        """
        winner = board.get_winner()
        moves = board.get_available_moves()
        score = self.get_score(board)
        return Evaluation(winner=winner, moves=moves, score=score)

    @abc.abstractmethod
    def get_score(self, board):
        """Return the score for a board.

        :param zerosum.base.Board board: the board to score
        :return: the score
        :rtype: float
        """


class Evaluation:

    def __init__(self, winner=None, moves=False, score=None):
        """An evaluation of a board.

        :param winner: the winning player
        :type winner: :class:`~zerosum.base.player.Player`
        :param list moves: the moves available on the board
        :param float score: the current score of the board
        """
        self.winner = winner
        self.score = score
        self.moves = moves

    @property
    def is_final(self):
        """True if the game is over."""
        return self.winner or not bool(self.moves)

    @property
    def is_win(self):
        """True if the game has a winner."""
        return bool(self.winner)

    @property
    def is_draw(self):
        """True if the game is over but there is no winner."""
        return not self.is_win and self.is_final

    def __bool__(self):
        """True if the game is over."""
        return self.is_final

    def __str__(self):
        if self.is_win:
            return '{} wins'.format(self.winner)
        elif self.is_draw:
            return "a draw"
        else:
            return '{} for the current player'.format(self.score)

    def __repr__(self):
        r = 'Evaluation(winner={!r}, is_final={!r}, score={!r})'
        return r.format(self.winner, self.is_final, self.score)
