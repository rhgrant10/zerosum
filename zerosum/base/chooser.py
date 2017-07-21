# -*- coding: utf-8 -*-
"""Strategy for choosing a move among those available."""
import itertools
import random


class Chooser:

    def _get_score_filter(self, score):
        return lambda scored_move: scored_move[0] == score

    def get_choice(self, sorted_scored_moves):
        """Return the chosen scored move from the sorted, scored moves.

        By default, this method chooses randomly among the moves with the
        "best" score among those given. Effectively, this avoids AI Players
        being destined to always make the same choices.

        :param list sorted_scored_moves: moves in order from "best" to "worst"
        :return: the chosen move among those given
        :rtype: tuple
        """
        top_score, __ = sorted_scored_moves[0]
        has_top_score = self._get_score_filter(score=top_score)
        best = list(itertools.takewhile(has_top_score, sorted_scored_moves))
        return random.choice(best)

    def get_min(self, scored_moves):
        """Return the minimum move.

        :param list scored_moves: available moves with scores
        :return: the minimum of the given moves
        :rtype: tuple
        """
        return self.get_choice(sorted(scored_moves))

    def get_max(self, scored_moves):
        """Return the maximum move.

        :param list scored_moves: available moves with scores
        :return: the maximum of the given moves
        :rtype: tuple
        """
        return self.get_choice(sorted(scored_moves, reverse=True))
