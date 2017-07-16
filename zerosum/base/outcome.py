# -*- coding: utf-8 -*-


class Outcome:
    def __init__(self, winner=None, is_over=False):
        self.winner = winner
        self.is_over = bool(winner) or is_over

    @classmethod
    def draw(cls):
        return cls(winner=None, is_over=True)

    @classmethod
    def win(cls, player):
        return cls(winner=player, is_over=True)

    @classmethod
    def none(cls):
        return cls(winner=None, is_over=False)

    @property
    def is_win(self):
        return bool(self.winner)

    @property
    def is_draw(self):
        return not self.winner and self.is_over

    def __bool__(self):
        return self.is_over

    def __str__(self):
        if self.is_win:
            return '{} wins!'.format(self.winner)
        elif self.is_draw:
            return "It's a draw..."
        else:
            return "It ain't over until it's over."
