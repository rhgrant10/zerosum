# -*- coding: utf-8 -*-
import math

import zerosum


class AlphaBeta(zerosum.base.Solver):

    def search(self, board, alpha=-math.inf, beta=math.inf, depth=0):
        print(board)
        evaluation = self.evaluator.evaluate(board)
        if evaluation.is_final or self.is_at_max_depth(depth):
            return evaluation.score, None

        scores = []
        for move in evaluation.moves:
            possible_board = board.make_move(move)
            score, __ = self.search(possible_board, alpha=-beta, beta=-alpha,
                                    depth=depth + 1)
            score = -score
            if score >= beta:
                return beta, move
            if score > alpha:
                alpha = score
            scores.append(score)

        scored_moves = zip(scores, evaluation.moves)
        return self.chooser.get_max(scored_moves)
