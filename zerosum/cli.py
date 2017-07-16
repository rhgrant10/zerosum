# -*- coding: utf-8 -*-
"""Console script for zerosum."""
import collections

import click

import zerosum


@click.command()
@click.option('-d', '--max-depth', type=int, default=10)
def main(max_depth):
    """Console script for zerosum."""
    evaluator = zerosum.examples.tictactoe.Evaluator()
    solver = zerosum.solvers.Minimax(evaluator, max_depth=max_depth)

    results = collections.Counter()
    for row in range(3):
        for col in range(3):
            print('Game {}'.format(row * 3 + col))
            board = zerosum.examples.tictactoe.Board()
            board = board.make_move([row, col])
            while not board.outcome:
                move = solver.get_best_move(board)
                print_board(board, '{} moves {}'.format(board.player, move))
                board = board.make_move(move)

            print_board(board, 'Result: {}'.format(board.outcome))
            results[str(board.outcome)] += 1

    print('\n{:18s} {:s}'.format('Result', 'Times'))
    print('~' * 24)
    for result, count in results.most_common():
        print('{:18s} {:d}'.format(result, count))


def print_board(board, message=None):
    print(board)
    if message:
        print(message)


if __name__ == "__main__":
    main()
