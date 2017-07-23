# -*- coding: utf-8 -*-
import zerosum


class Negamax(zerosum.base.Solver):

    def __init__(self, evaluator, chooser=None, max_depth=None):
        if chooser is None:
            chooser = zerosum.base.chooser.Random()
        super().__init__(evaluator=evaluator, chooser=chooser,
                         max_depth=max_depth)

    def get_best_move(self, board):
        __, move = self._negamax(board)
        return move

    def _negamax(self, board, depth=0):
        evaluation = self.evaluator.evaluate(board)
        if evaluation.is_final or self.is_at_max_depth(depth):
            return evaluation.score, None

        scores = []
        for move in evaluation.moves:
            possible_board = board.make_move(move)
            score, __ = self._negamax(possible_board, depth=depth + 1)
            scores.append(-score)

        scored_moves = zip(scores, evaluation.moves)
        return self.chooser.get_max(scored_moves)
