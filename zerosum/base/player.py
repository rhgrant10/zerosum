# -*- coding: utf-8 -*-
import re

import faker


class PlayerError(Exception):
    def __init__(self, message, player):
        super().__init__(message)
        self.player = player


class IQuitError(PlayerError):
    def __init__(self, player):
        message = '{!r} quits'.format(player)
        super().__init__(message=message, player=player)


class InvalidMove(PlayerError):
    def __init__(self, player, move):
        message = 'Invalid move {!r} from {!r}'.format(move, player)
        super().__init__(message=messsage, player=player)
        self.move = move


class Player:
    def __init__(self, name):
        self.name = name

    def take_turn(self, board, move):
        return board.make_move(move)

    def quit(self):
        raise IQuitError(player=self)

    def __repr__(self):
        return 'Player(name={!r})'.format(self.name)

    def __str__(self):
        return self.name


class AiPlayer(Player):
    def __init__(self, solver, name=None):
        self.solver = solver
        if not name:
            fake = faker.Faker()
            name = fake.name()
        super().__init__(name=name)

    def take_turn(self, board):
        move = self.solver.get_best_move(board)
        return super().take_turn(board, move)


class HumanPlayer(Player):
    move_re = re.compile(r'''^(?P<row>[012]).+(?P<column>[012])$''')

    def __init__(self, name, move_re=None):
        super().__init__(name=name)
        self.move_re = move_re or self.move_re

    def is_quit(self, response):
        return response.lower() == 'q'

    def get_input(self):
        return input()

    def parse_input(self, response):
        if self.is_quit(response):
            self.quit()

        match = self.move_re.match(response)
        if match:
            return match.group('row'), match.group('column')

        raise InvalidMove(player=self, move=response)

    def take_turn(self, board):
        response = self.get_input()
        move = self.parse_input(response)
        return super().take_turn(board, move)
