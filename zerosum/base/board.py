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
