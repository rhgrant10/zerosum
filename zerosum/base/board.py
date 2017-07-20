# -*- coding: utf-8 -*-
import abc


class Board(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def make_move(self, move):
        """Make a move and return the resulting ``zerosum.Board``.

        No changes are made to the board. Instead, a new copy of the board is
        returned.

        :param tuple move: the move to make
        :return: the board after the move has been made
        :rtype: `zerosum.Board`
        """

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
    def is_game_over(self):
        """"""
