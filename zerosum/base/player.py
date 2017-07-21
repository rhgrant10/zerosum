# -*- coding: utf-8 -*-
import abc
import faker

from zerosum import exceptions


class Player:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Player(name={!r})'.format(self.name)

    def __str__(self):
        return self.name

    def take_turn(self, board):
        self.take_pre_turn(board)
        move = self.get_move(board)
        try:
            return board.make_move(move)
        except ValueError as e:
            raise exceptions.InvalidMove(player=self, move=move) from e

    def take_pre_turn(self, board):
        pass

    def quit(self):
        raise exceptions.IQuitError(player=self)

    @abc.abstractmethod
    def get_move(self):
        pass


class AiPlayer(Player):
    def __init__(self, solver, name=None):
        self.solver = solver
        name = name or self.__class__.get_fake_name()
        super().__init__(name=name)

    def get_move(self, board):
        return self.solver.get_best_move(board)

    @classmethod
    def get_fake_name(cls):
        fake = faker.Faker()
        return fake.name()


class HumanPlayer(Player):

    def get_move(self, board):
        response = self.get_input()
        if self.is_quit(response):
            self.quit()
        return self.parse_move_input(response)

    def is_quit(self, response):
        pass

    @abc.abstractmethod
    def get_input(self):
        pass

    @abc.abstractmethod
    def parse_move_input(self, response):
        pass
