import flask
from flask import Flask, request, jsonify, make_response
from game import Teeko2Player
app = Flask(__name__)


@app.route('/ai-move/', methods=['GET'])
def respond():
    boardStr = request.args.get("board", "")
    response = {}
    if len(boardStr) != 25:
        response["ERROR"] = "Board isn't the right length"
    # Calculate the board and next move for ai
    else:
        board = get_board_from_request(boardStr)
        ai = Teeko2Player(board)
        move = ai.make_move(ai.board)
        ai.place_piece(move, 'r')

        print(f"Received Board: {board}")
        print(f"Move: {move}")
        print(f"Returned: {board}")

        response["move"] = move
        response["board"] = get_response_board_string(ai.board)
    resp = make_response(response)
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def get_board_from_request(boardStr):
    board = [[' ' for j in range(5)] for i in range(5)]
    for i in range(5):
        for j in range(5):
            if boardStr[(i * 5) + j] == 's':
                board[i][j] = ' '
            else:
                board[i][j] = boardStr[(i * 5) + j]
    return board


def get_response_board_string(board):
    boardString = ""
    for i in range(5):
        for j in range(5):
            if board[i][j] == ' ':
                boardString += 's'
            else:
                boardString += board[i][j]
    return boardString


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our Teeko AI API</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)