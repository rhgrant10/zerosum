# -*- coding: utf-8 -*-
import abc
import math
import sys

from .evaluator import Evaluator


class Solver(metaclass=abc.ABCMeta):
    def __init__(self, evaluator, max_depth=None):
        self.evaluator = evaluator
        self.max_depth = max_depth
        
    def is_at_max_depth(self, depth):
        return self.max_depth and depth >= self.max_depth

    @abc.abstractmethod
    def get_best_move(self, board):
        pass


class Minimax(Solver):
    def get_best_move(self, board):
        __, best_move = self._maxi(board)
        return best_move

    def _maxi(self, board, depth=0):
        if board.outcome or self.is_at_max_depth(depth):
            score = self.evaluator.score(board, depth=depth)
            return score, None

        moves = board.get_available_moves()
        scores = []
        for move in moves:
            possible_board = board.make_move(move)
            score, __ = self._mini(possible_board, depth=depth + 1)
            scores.append(score)

        scored_moves = zip(scores, moves)
        best_scored_moves = list(sorted(scored_moves, reverse=True))
        return best_scored_moves[0]

    def _mini(self, board, depth=0):
        if board.outcome or self.is_at_max_depth(depth):
            score = self.evaluator.score(board, depth=depth)
            return -score, None

        moves = board.get_available_moves()
        scores = []
        for move in moves:
            possible_board = board.make_move(move)
            score, __ = self._maxi(possible_board, depth=depth + 1)
            scores.append(score)

        scored_moves = zip(scores, moves)
        best_scored_moves = list(sorted(scored_moves))
        return best_scored_moves[0]
