from flask import Flask, request, jsonify
from game import Teeko2Player
app = Flask(__name__)


@app.route('/ai-move/', methods=['GET'])
def respond():
    print("testing api")
    # Retrieve the name from the url parameter /getmsg/?name=
    boardStr = request.args.get("board", "")
    print(f"Received: {boardStr}")
    board = [[' ' for j in range(5)] for i in range(5)]
    response = {'Content-Type': 'application/json'}
    response.headers['Access-Control-Allow-Origin'] = '*'
    # Check if the board isn't the right length
    if len(boardStr) != 25:
        response["ERROR"] = "Board isn't the right length"
    # Calculate the board and next move for ai
    else:
        for i in range(5):
            for j in range(5):
                playerInt = boardStr[(i * 5) + j]
                playerInt = int(playerInt)
                playerChar = ' '
                if playerInt == 1:
                    playerChar = 'r'
                elif playerInt == 2:
                    playerChar = 'b'
                board[i][j] = playerChar
        ai = Teeko2Player(board)
        move = ai.make_move(ai.board)
        response["move"] = move

    # Return the response in json format
    return jsonify(response)


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our Teeko AI API</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)