# -*- coding: utf-8 -*-
from flask import jsonify
from flask import request
from flask import abort
from flask import render_template

from app import app
from zerosum import solvers
from zerosum import base
from zerosum.examples import tictactoe


solvers_map = {
    'minimax': solvers.Minimax,
    'negamax': solvers.Negamax,
    'alphabeta': solvers.AlphaBeta,
}


evaluators_map = {
    'smart': tictactoe.SmartEvaluator,
    'simple': tictactoe.SimpleEvaluator,
}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/about')
def api_description():
    description = {
        '/api/search/': {
            'evaluators': list(evaluators_map),
            'solvers': list(solvers_map),
            'maxDepth': list(range(10)),
        }
    }
    return jsonify(description)


@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    if not data or 'board' not in data or 'players' not in data:
        abort(400)

    board = tictactoe.Board(squares=data['board'], players=data['players'])

    Evaluator = evaluators_map[data.get('evaluator', 'smart')]
    Solver = solvers_map[data.get('solver', 'minimax')]
    max_depth = data.get('maxDepth', 5)

    solver = Solver(evaluator=Evaluator(), max_depth=max_depth)
    scored_move = solver.search(board)
    result = dict(zip(['score', 'move'], scored_move))

    response = {
        'result': result,
        'solver': Solver.__name__,
        'evaluator': Evaluator.__name__,
        'maxDepth': max_depth,
    }
    return jsonify(response)
