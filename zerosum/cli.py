# -*- coding: utf-8 -*-
"""Console script for zerosum."""
import collections

import click

from zerosum.examples import tictactoe
from zerosum.base import Game


@click.command()
@click.option('--max-depth', type=int, default=5, show_default=True,
              help='maximum depth for the solver')
@click.option('--smart/--simple', default=True, show_default=True,
              help='which board evaluator to use')
def main(max_depth, smart):
    """Console script for zerosum."""

    # Create the players
    name = input("What's your name? ")
    human = tictactoe.HumanPlayer(name=name)
    if smart:
        computer = tictactoe.SmartPlayer(max_depth=max_depth)
    else:
        computer = tictactoe.SimplePlayer(max_depth=max_depth)

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
