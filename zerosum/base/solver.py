# -*- coding: utf-8 -*-
import abc
import zerosum


class Solver(metaclass=abc.ABCMeta):
    def __init__(self, evaluator, chooser=None, max_depth=None):
        self.evaluator = evaluator
        self.chooser = chooser or zerosum.base.chooser.Random()
        self.max_depth = max_depth

    def __repr__(self):
        return ('Solver(evaluator={0.evaluator!r}, chooser={0.chooser!r}, '
                'max_depth={0.max_depth!r}'.format(self))

    def is_at_max_depth(self, depth):
        return self.max_depth and depth >= self.max_depth

    def get_best_move(self, board):
        __, move = self.search(board)
        return move

    @abc.abstractmethod
    def search(self, board):
        pass
