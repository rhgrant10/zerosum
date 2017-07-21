# -*- coding: utf-8 -*-
"""Console script for zerosum."""
import collections

import click

from zerosum.examples import tictactoe
from zerosum.base import Game


@click.command()
@click.option('-d', '--max-depth', type=int, default=10)
def main(max_depth):
    """Console script for zerosum."""

    # Create the players
    name = input("What's your name? ")
    human = tictactoe.HumanPlayer(name=name)
    computer = tictactoe.SmartPlayer()

    # Figure out who's first
    answer = True
    while answer and answer not in ('y', 'yes', 'n', 'no'):
        answer = input('(Yes/no) Do you want to be X? ')

    if not answer or 'y' in answer:
        players = human, computer
    else:
        players = computer, human

    # Play the game
    board = tictactoe.Board()
    game = tictactoe.Game(players=players, board=board)
    winner = game.play()

    # Report the result.
    if winner == Game.DRAW:
        print("It's a draw!")
    elif winner:
        print('{} wins!'.format(winner))


if __name__ == "__main__":
    main()
