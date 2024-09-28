import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

@app.route('/klotski', methods=['POST'])
def evaluate_klotski():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    boards = []
    moves = []
    for item in data:
        boards.append(item.get("board"))
        moves.append(item.get("move"))
    
    solved = []
    for i in range(len(boards)):
        board_matrix = parse_board_to_matrix(boards[i])
        move = moves[i]
        for j in range(0, len(move), 2):
            block = move[j]
            direction = move[j+1]
            for k in range(len(board_matrix)):
                for l in range(len(board_matrix[0])):
                    if board_matrix[k][l] == block:
                        if direction == 'N':
                            board_matrix[k-1][l] = block
                            board_matrix[k][l] = '@'
                        elif direction == 'E':
                            board_matrix[k][l+1] = block
                            board_matrix[k][l] = '@'
                        elif direction == 'S':
                            board_matrix[k+1][l] = block
                            board_matrix[k][l] = '@'
                        elif direction == 'W':
                            board_matrix[k][l-1] = block
                            board_matrix[k][l] = '@'
       
        # Flatten the matrix into a single string
        solved_matrix = ''.join(''.join(row) for row in board_matrix)
        solved.append(solved_matrix)
    
    # to be updates
    logging.info("My result :{}".format(solved))
    return json.dumps(solved)


def parse_board_to_matrix(board_str, rows=5, cols=4):
    # Split the board string into chunks of 'cols' length for each row
    board_matrix = [list(board_str[i:i+cols]) for i in range(0, len(board_str), cols)]
    return board_matrix