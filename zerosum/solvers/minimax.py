from zerosum.base import Solver


class Minimax(Solver):

    def get_best_move(self, board):
        """Return the best move on a board.

        :param zerosum.board.Board board: a game board
        :return: the best move as a 0-indexed row and column
        :retype: tuple
        """
        __, best_move = self._maxi(board)
        return best_move

    def _maxi(self, board, depth=0):
        # maximize the score
        if board.outcome.is_over or self.is_at_max_depth(depth):
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
        # minimize the score
        if board.outcome.is_over or self.is_at_max_depth(depth):
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
