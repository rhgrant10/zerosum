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
        winner = self.get_winner(board)
        moves = self.get_available_moves(board)
        score = self.get_score(board)
        return Evaluation(winner=winner, moves=moves, score=score)

    @abc.abstractmethod
    def get_available_moves(self):
        """Return all available moves on the board for the current player.

        :return: all available moves
        :rtype: list
        """

    @abc.abstractmethod
    def get_winner(self):
        """Return the winner, if any.

        :return: the winner or ``None`` if there is no winner
        """

    @abc.abstractmethod
    def get_score(self, board):
        """Return the score for a board.

        :param zerosum.base.Board board: the board to score
        :return: the score
        :rtype: float
        """


class Evaluation:

    def __init__(self, winner=None, moves=False, score=None):
        self.winner = winner
        self.score = score
        self.moves = moves

    @property
    def is_final(self):
        return not bool(self.moves)

    @property
    def is_win(self):
        return bool(self.winner)

    @property
    def is_draw(self):
        return not self.is_win and self.is_final

    def __bool__(self):
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
