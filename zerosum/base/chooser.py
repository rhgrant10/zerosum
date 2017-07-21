# -*- coding: utf-8 -*-
import itertools
import random


class Chooser:
    def get_score_filter(self, score):
        return lambda scored_move: scored_move[0] == score

    def get_best(self, sorted_scored_moves):
        top_score, __ = sorted_scored_moves[0]
        has_top_score = self.get_score_filter(score=top_score)
        best = list(itertools.takewhile(has_top_score, sorted_scored_moves))
        return random.choice(best)

    def get_min(self, scored_moves):
        return self.get_best(sorted(scored_moves))

    def get_max(self, scored_moves):
        return self.get_best(sorted(scored_moves, reverse=True))
