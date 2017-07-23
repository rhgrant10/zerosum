# -*- coding: utf-8 -*-
import math

import zerosum


class AlphaBeta(zerosum.base.Solver):
    def __init__(self, evaluator, chooser=None, max_depth=None):
        if chooser is None:
            chooser = zerosum.base.chooser.Random()
        super().__init__(evaluator=evaluator, chooser=chooser,
                         max_depth=max_depth)

    def get_best_move(self, board):
        __, move = self._alphabeta(board)
        return move

    def _alphabeta(self, board, alpha=-math.inf, beta=math.inf, depth=0):
        evaluation = self.evaluator.evaluate(board)
        if evaluation.is_final or self.is_at_max_depth(depth):
            return evaluation.score, None

        scores = []
        for move in evaluation.moves:
            possible_board = board.make_move(move)
            score, __ = self._alphabeta(possible_board, alpha=-beta,
                                        beta=-alpha, depth=depth + 1)
            score = -score
            if score >= beta:
                return beta, move
            if score > alpha:
                alpha = score
            scores.append(score)

        scored_moves = zip(scores, evaluation.moves)
        return self.chooser.get_max(scored_moves)
