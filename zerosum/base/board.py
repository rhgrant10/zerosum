# -*- coding: utf-8 -*-
import abc

from zerosum import base


class Board(metaclass=abc.ABCMeta):
    #: The winner, draw, or None
    outcome = property(lambda self: self.get_outcome())

    def get_outcome(self):
        """Return the outcome of the board.

        If a player has won, the player is returned. If the game is a draw,
        ``DRAW`` is returned. If the game is still in progress, ``None`` is
        returned.

        :return: the outcome of the board or ``None``
        """
        winner = self.get_winner()
        no_moves_left = not bool(self.get_available_moves())
        return base.Outcome(is_over=no_moves_left, winner=winner)

    @abc.abstractmethod
    def get_available_moves(self):
        """Return all available moves on the board for the current player.

        :return: all available moves
        :rtype: list
        """

    @abc.abstractmethod
    def make_move(self, move):
        """Make a move and return the resulting ``zerosum.Board``.

        No changes are made to the board. Instead, a new copy of the board is
        returned.

        :param tuple move: the move to make
        :return: the board after the move has been made
        :rtype: `zerosum.Board`
        """
