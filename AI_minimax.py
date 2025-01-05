import constants as c
import random
import logic as lc

MAX_DEPTH = 3

moves = {
    'Up': lc.up,
    'Down': lc.down,
    'Left': lc.left,
    'Right': lc.right
}

def expectimax_move(matrix):
    best_move = None
    best_score = -float('inf')

    # Evaluate all possible moves (max nodes)
    for move_key in moves:
        new_matrix, done, points = moves[move_key](matrix)  # Call the function
        if done:
            score = expectimax(new_matrix, depth=0, maximizing_player=False)
            # Keep track of the best move based on the score
            if score > best_score:
                best_score = score
                best_move = move_key
    return best_move

def expectimax(matrix, depth, maximizing_player):
    # Return the heuristic value of the board if maximum depth is reached or the game is over.
    if depth == MAX_DEPTH or lc.game_state(matrix) != 'not over':
        return evaluate_board(matrix)
    
    if maximizing_player:
        # Max node: player's turn (maximize score)
        best_score = -float('inf')
        for move_key in moves:
            new_matrix, done, points = moves[move_key](matrix)
            if done:
                score = expectimax(new_matrix, depth + 1, False)
                best_score = max(best_score, score)
        return best_score
    
    else:
        # Chance node: AI's turn (expectation over random tiles)
        empty_cells = get_empty_cells(matrix)
        if not empty_cells:
            return evaluate_board(matrix)
        
        total_score = 0
        for cell in empty_cells:
            row, col = cell
            # Test both the '2' and '4' possibilities
            for value in [2, 4]:
                new_matrix = place_random_tile(matrix, row, col, value)
                probability = 0.9 if value == 2 else 0.1  # 90% chance of 2, 10% chance of 4
                total_score += probability * expectimax(new_matrix, depth + 1, True)

        return total_score / len(empty_cells)

def evaluate_board(matrix):
    return sum(sum(row) for row in matrix)  # The higher the sum of tiles, the better

def get_empty_cells(matrix):  # Returns a list of empty cells (row, col) in the grid
    empty_cells = []
    for i in range(c.GRID_LEN):
        for j in range(c.GRID_LEN):
            if matrix[i][j] == 0:
                empty_cells.append((i, j))
    return empty_cells

def place_random_tile(matrix, row, col, value):  # Simulates placing a random tile (2 or 4) at a specific location in the matrix
    new_matrix = [row[:] for row in matrix]
    new_matrix[row][col] = value
    return new_matrix

def AI_play(matrix):
    move_key = expectimax_move(matrix)
    if move_key == 'Up':
        return c.KEY_UP
    elif move_key == 'Down':
        return c.KEY_DOWN
    elif move_key == 'Left':
        return c.KEY_LEFT
    elif move_key == 'Right':
        return c.KEY_RIGHT
