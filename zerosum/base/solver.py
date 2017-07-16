# -*- coding: utf-8 -*-
import abc


class Solver(metaclass=abc.ABCMeta):
    def __init__(self, evaluator, chooser, max_depth=None):
        self.evaluator = evaluator
        self.chooser = chooser
        self.max_depth = max_depth

    def is_at_max_depth(self, depth):
        return self.max_depth and depth >= self.max_depth

    @abc.abstractmethod
    def get_best_move(self, board):
        pass
