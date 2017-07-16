import itertools

import zerosum


class Minimax(zerosum.base.Solver):
    def __init__(self, evaluator, chooser=None, max_depth=None):
        if chooser is None:
            chooser = zerosum.base.Chooser()
        super().__init__(evaluator=evaluator, chooser=chooser,
                         max_depth=max_depth)

    def get_best_move(self, board):
        __, best_move = self._maxi(board)
        return best_move

    def _maxi(self, board, depth=0):
        # maximize the score
        evaluation = self.evaluator.evaluate(board)
        if evaluation.is_final or self.is_at_max_depth(depth):
            return evaluation.score, None

        scores = []
        for move in evaluation.moves:
            possible_board = board.make_move(move)
            score, __ = self._mini(possible_board, depth=depth + 1)
            scores.append(score)

        scored_moves = zip(scores, evaluation.moves)
        return self.chooser.get_max(scored_moves)

    def _mini(self, board, depth=0):
        # minimize the score
        evaluation = self.evaluator.evaluate(board)
        if evaluation.is_final or self.is_at_max_depth(depth):
            return evaluation.score, None

        scores = []
        for move in evaluation.moves:
            possible_board = board.make_move(move)
            score, __ = self._maxi(possible_board, depth=depth + 1)
            scores.append(score)

        scored_moves = zip(scores, evaluation.moves)
        return self.chooser.get_min(scored_moves)
