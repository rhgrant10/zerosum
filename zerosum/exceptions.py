# -*- coding: utf-8 -*-


class ZerosumError(Exception):
    pass


class PlayerError(ZerosumError):
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
        super().__init__(message=message, player=player)
        self.move = move

