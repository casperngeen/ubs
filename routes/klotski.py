import json
import logging
import copy

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
        moves.append(item.get("moves"))
    
    solved = []
    for i in range(len(boards)):
        board_matrix = parse_board_to_matrix(boards[i])
        size = {}
        for j in range(5):
            for k in range(4):
                if board_matrix[j][k] not in size:
                    row, col = j, k
                    while row < 5 and board_matrix[row][k] == board_matrix[j][k]:
                        row += 1
                    while col < 4 and board_matrix[j][col] == board_matrix[j][k]:
                        col += 1
                    size[board_matrix[j][k]] = [row-j, col-k]            
        move = moves[i]
        print(size)
        for j in range(0, len(move), 2):
            block = move[j]
            direction = move[j+1]
            logging.info(j)
            logging.info("Block: {}, Direction: {}".format(block, direction))
            found = False
            for k in range(len(board_matrix)):
                for l in range(len(board_matrix[0])):
                    if board_matrix[k][l] == block:
                        logging.info("Row: {}, Col: {}".format(k, l))
                        found = True
                        if direction == 'N':
                            for a in range(size[block][1]):
                                board_matrix[k-1][l+a] = block
                                board_matrix[k+size[block][0]-1][l+a] = '@'
                        elif direction == 'E':
                            for a in range(size[block][0]):
                                board_matrix[k+a][l+size[block][1]] = block
                                board_matrix[k+a][l] = '@'
                        elif direction == 'S':
                            for a in range(size[block][1]):
                                board_matrix[k+size[block][0]][l+a] = block
                                board_matrix[k][l+a] = '@'
                        elif direction == 'W':
                            for a in range(size[block][0]):
                                board_matrix[k+a][l-1] = block
                                board_matrix[k+a][l+size[block][0]-1] = '@'
                        break
                if found:
                    break
            print_matrix(board_matrix)
       
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

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))