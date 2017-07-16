# -*- coding: utf-8 -*-
"""Console script for zerosum."""
import collections

import click

import zerosum


@click.command()
@click.option('-d', '--max-depth', type=int, default=10)
def main(max_depth):
    """Console script for zerosum."""
    evaluator = zerosum.examples.tictactoe.AllOrNothing()
    solver = zerosum.Minimax(evaluator, max_depth=max_depth)

    wins = collections.Counter()
    for row in range(3):
        for col in range(3):
            print('Game {}'.format(row * 3 + col))
            board = zerosum.examples.tictactoe.TicTacToe()
            board = board.make_move([row, col])
            while not board.outcome:
                print()
                print(board)
                print()
                move = solver.get_best_move(board)
                print(move)
                board = board.make_move(move)
            print()
            print(board)
            print('Result: {}'.format(board.outcome))
            wins[board.outcome] += 1

    print()
    print('Player    Wins')
    print('--------------')
    for player, count in wins.most_common():
        print('{:10s}{:d}'.format(player ,count))


if __name__ == "__main__":
    main()
