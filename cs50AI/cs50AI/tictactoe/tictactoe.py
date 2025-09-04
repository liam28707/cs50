"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for rows in board:
        for moves in rows:
            if moves != EMPTY:
                count += 1
    if count % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions.add((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    temp = copy.deepcopy(board)
    moves = actions(temp)
    if action not in moves:
        raise ValueError("Invalid Input")
    else:
        temp[action[0]][action[1]] = player(board)
    return temp


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Improved Logic(See Notes)
    for player in ['X', 'O']:
        # Check rows and columns
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
                return player

        # Check diagonals
        if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
            return player

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or not any(None in row for row in board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        value,move = max_value(board)
    elif player(board) == O:
        value,move = min_value(board)

    return move

def max_value(board):
    v = float('-inf')
    optimal = None
    if terminal(board):
        return utility(board), None
    for action in actions(board):
        value,_ = min_value(result(board,action))
        if value > v:
            v = value
            optimal = action
    return v,optimal
def min_value(board):
    v = float('inf')
    optimal = None
    if terminal(board):
        return utility(board),None
    for action in actions(board):
        value,_ = max_value(result(board,action))
        if value < v:
            v = value
            optimal = action
    return v,optimal






"""
NOTES


WINNER FUNCTION
    (First Logic)
    for i in range(len(board)):
        #Check for horizontal X & O
        if board[i][0] == board[i][1] == board[i][2] == X:
            return X
        elif board[i][0] == board[i][1] == board[i][2] == O:
            return O
        #Check for vertical X & O
        elif board[0][i] == board[1][i] == board[2][i] == X:
            return X
        elif board[0][i] == board[1][i] == board[2][i] == O:
            return O
        #Check for diagonals
        elif all(board[i][i] == X for i in range(3)):
            return X
        elif all(board[i][i] == O for i in range(3)):
            return O
        elif all(board[i][2-i] == X for i in range(3)):
            return X
        elif all(board[i][2-i] == O for i in range(3)):
            return O
        else:
            return None
        (First Logic)
"""