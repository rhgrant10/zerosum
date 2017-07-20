import abc
import itertools
import collections


class Game:
    DRAW = 'draw'

    def __init__(self, players, board):
        self.players = collections.OrderedDict(zip(board.players, players))
        self.boards = [board]

    @property
    def board(self):
        return self.boards[-1]
    @board.setter
    def board(self, board):
        self.boards.append(board)

    def play(self):
        introduction = '\n\t{} VS {}\n------------------------------------\n'
        print(introduction.format(*self.players.values()))
        for player in itertools.cycle(self.players.values()):
            if self.board.is_game_over():
                winner = self.board.get_winner()
                return self.players.get(winner, Game.DRAW)
            print("It's {}'s turn. Go.".format(player))
            self.board = player.take_turn(self.board)
            self.display()

    @abc.abstractmethod
    def display(self):
        print(self.board)
