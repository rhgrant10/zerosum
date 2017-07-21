import abc
import itertools
import collections

from zerosum import exceptions


class Game:
    DRAW = 'draw'

    def __init__(self, players, board):
        self.players = collections.OrderedDict(zip(board.players, players))
        self.boards = [board]
        self.player = None

    @property
    def board(self):
        return self.boards[-1]
    @board.setter
    def board(self, board):
        self.boards.append(board)

    def play(self):
        self.play_intro()
        for player in itertools.cycle(self.players.values()):
            self.player = player

            # First handle game over scenario.
            if self.board.is_game_over():
                winner = self.board.get_winner()
                return self.players.get(winner, Game.DRAW)

            # Now let the player take their turn.
            self.play_pre_turn()
            board = None
            while not board:
                try:
                    board = player.take_turn(self.board)
                except exceptions.InvalidMove as e:
                    self.play_invalid_move(e)
                except exceptions.IQuitError as e:
                    self.play_quit(e)
                    return None
            self.board = board
            self.play_post_turn()

    def play_invalid_move(self, e):
        pass

    def play_quit(self, e):
        pass

    def play_intro(self):
        pass

    def play_pre_turn(self):
        pass

    def play_post_turn(self):
        pass
