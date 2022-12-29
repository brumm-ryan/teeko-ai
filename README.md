# teeko-ai

## About the API 
This is a Flask API that calculates the optimal behavior for a Teeko player. 
The endpoint `/ai-move` accepts a query param `board` that is a 25 character string that represents a 5 x 5 board flattened. 
With each space of the board being one of the following 'r' => red player, 'b' => blue player, 's' => empty space.  
It calculates the best move according the methods/hueristics defined below and responds with 3 fields.
"board" => the state of the given board after the optimal move was made.
"move" => the optimal move that was preformed on the board
"win" => the winner of the game if applicable(-1 => player won, 1 => ai won, 0 => no winner yet).


## About the Teeko AI
Given a board of Teeko (aka state) we calculate possible future states based on all possible moves. 
We rate the condition of a state using a hueristic that is based on a number of factors such as how many pieces in a row you have versus your opponenet.
We then use a Min/Max optimization algorithm to recursively maximize the future possible states to predict the next best move.

## Test out the API -> https://teeko-ai-backend.herokuapp.com/ai-move/?board=sssssssssssbssssrssssssss

## Try the web app -> https://brumm-ryan.github.io/teeko-web-app/

## Web App Repo -> https://github.com/brumm-ryan/teeko-web-app
