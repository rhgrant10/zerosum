# -*- coding: utf-8 -*-
import abc


class Evaluator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def score(self, board, depth=0):
        pass
