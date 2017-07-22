# -*- coding: utf-8 -*-
import itertools
import collections

from zerosum import exceptions


class Game:
    DRAW = 'draw'

    def __init__(self, players, board):
        """A Zero Sum Game with players and a board.

        :param list players: the (two) game players
        :param board: the game board
        :type board: :class:`zerosum.base.Board`
        """
        self.players = collections.OrderedDict(zip(board.players, players))
        self.player = None
        self.history = [board]

    def __repr__(self):
        return 'Game(players={0.players!r}, board={0.board!r})'.format(self)

    @property
    def board(self):
        """The current board for the game."""
        return self.history[-1]

    def play(self):
        self.intro_hook()
        for player in itertools.cycle(self.players.values()):
            # Let self.player always refer to the current player
            self.player = player

            # First handle the game over scenario.
            if self.board.is_game_over():
                winner = self.board.get_winner()
                return self.players.get(winner, Game.DRAW)

            self.pre_turn_hook()

            # Now let the player take their turn.
            board = None
            while not board:
                try:
                    board = self.player.take_turn(self.board)
                except exceptions.InvalidMove as e:
                    self.invalid_move_hook(e)
                except exceptions.IQuitError as e:
                    self.player_quit_hook(e)
                    return None

            # Add the resulting board to the game history.
            self.history.append(board)

            self.post_turn_hook()

    def intro_hook(self):
        """Perform any pre-game actions."""

    def pre_turn_hook(self):
        """Perform tasks just before a player takes a turn."""

    def post_turn_hook(self):
        """Perform tasks just after a player takes a turn."""

    def invalid_move_hook(self, e):
        """Perform tasks when a player chooses an invalid move."""

    def player_quit_hook(self, e):
        """Perform tasks when a player chooses to quit."""
