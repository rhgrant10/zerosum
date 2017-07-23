# -*- coding: utf-8 -*-
import zerosum


class Negamax(zerosum.base.Solver):

    def search(self, board, depth=0):
        evaluation = self.evaluator.evaluate(board)
        if evaluation.is_final or self.is_at_max_depth(depth):
            return evaluation.score, None

        scores = []
        for move in evaluation.moves:
            possible_board = board.make_move(move)
            score, __ = self.search(possible_board, depth=depth + 1)
            scores.append(-score)

        scored_moves = zip(scores, evaluation.moves)
        return self.chooser.get_max(scored_moves)
