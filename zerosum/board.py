import abc


class Board(metaclass=abc.ABCMeta):
    outcome = property(lambda self: self.get_outcome())

    @abc.abstractmethod
    def get_outcome(self):
        pass
