import constants as c
import random
import logic as lc

MAX_DEPTH = 3
commands = {
    'Up': lc.up,
    'Down': lc.down,
    'Left': lc.left,
    'Right': lc.right
}

moves = {
    'Up': lc.up,
    'Down': lc.down,
    'Left': lc.left,
    'Right': lc.right
}

def AI_play(matrix, weights):
    move_key = expectimax_move(matrix, weights)
    if move_key == 'Up':
        return c.KEY_UP
    elif move_key == 'Down':
        return c.KEY_DOWN
    elif move_key == 'Left':
        return c.KEY_LEFT
    elif move_key == 'Right':
        return c.KEY_RIGHT
    
##################################################
################### Heuristics ###################
##################################################
def corner_heuristic(matrix):
    max_tile = 0
    max_pos = (0, 0)

    # Find the largest tile and its position
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] > max_tile:
                max_tile = matrix[i][j]
                max_pos = (i, j)

    # Check if the largest tile is in a corner
    if max_pos in [(0, 0), (0, len(matrix) - 1), (len(matrix) - 1, 0), (len(matrix) - 1, len(matrix) - 1)]:
        return 1 # Reward for having largest tile in a corner
    else:
        return 0


################### Monotonicity heuristic ###################
'Evaluates the smoothness of the board aka how consistently the tile values increase or decrease across rows and columns'
def monotonicity_heuristic(matrix):
    score = 0

    # Check rows for monotonicity (both left-to-right and right-to-left)
    for row in matrix:
        for i in range(len(row) - 1):
            if row[i] >= row[i + 1]:
                score += row[i] - row[i + 1]
            else:
                score -= (row[i + 1] - row[i])

    # Check columns for monotonicity (top-to-bottom & bottom-to-top)
    for j in range(len(matrix)):
        for i in range(len(matrix) - 1):
            if matrix[i][j] >= matrix[i + 1][j]:
                score += matrix[i][j] - matrix[i + 1][j]
            else:
                score -= (matrix[i + 1][j] - matrix[i][j])

    return score

################### Smoothness heuristic ###################
# This heuristic rewards grids where adjacent tiles have similar values.
# The lower the difference between adjacent tiles, the better.
def smoothness_heuristic(matrix):
    smoothness_score = 0

    # Check horizontal neighbors for smoothness
    for row in matrix:
        for i in range(len(row) - 1):
            if row[i] != 0 and row[i + 1] != 0:
                smoothness_score -= abs(row[i] - row[i + 1])  # Penalize larger differences

    # Check vertical neighbors for smoothness
    for col in range(len(matrix[0])):
        for i in range(len(matrix) - 1):
            if matrix[i][col] != 0 and matrix[i + 1][col] != 0:
                smoothness_score -= abs(matrix[i][col] - matrix[i + 1][col])  # Penalize larger differences

    return smoothness_score

################### Merging Potential ###################
" If two adjacent tiles can be merged in the next move, the heuristic will prioritize such moves"

def merging_heuristic(matrix):
    merge_score = 0

    # Horizontal pairs
    for i in range(len(matrix)):
        for j in range(len(matrix[0]) - 1):
            if matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0:
                merge_score  += matrix[i][j]


    # Vertical pairs
    for i in range(len(matrix) - 1):
        for j in range(len(matrix[0])):
            if matrix[i][j] == matrix[i + 1][j] and matrix [i][j] != 0:
                merge_score += matrix[i][j]

    return merge_score


################### Empty spaces heuristic###################
def count_empty_spaces(matrix):
    return sum(row.count(0) for row in matrix)

def evaluate_empty_spaces(matrix):
    return count_empty_spaces(matrix)


################### Clustering heuristic###################
'How close similar tiles are to one another'
def clustering_heuristic(matrix): 
    clustering_score = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0]) - 1):
            if matrix[i][j] != 0 and matrix[i][j + 1] != 0:
                clustering_score -= abs(matrix[i][j] - matrix[i][j + 1])
    for j in range(len(matrix[0])):
        for i in range(len(matrix) - 1):
            if matrix[i][j] != 0 and matrix[i + 1][j] != 0:
                clustering_score -= abs(matrix[i][j] - matrix[i + 1][j])
    return clustering_score


##################################################
################### Expectimax ###################
##################################################
def expectimax_move(matrix, weights):
    best_move = None
    best_score = -float('inf')

    # Evaluate all possible moves (max nodes)
    for move_key in moves:
        new_matrix, done, points = moves[move_key](matrix)  # Call the function
        if done:
            score = expectimax(new_matrix, weights, depth=-2, maximizing_player=False)
            # Keep track of the best move based on the score
            if score > best_score:
                best_score = score
                best_move = move_key
    return best_move

def expectimax(matrix, weights, depth, maximizing_player=False):
    # Return the heuristic value of the board if maximum depth is reached or the game is over.
    if depth == MAX_DEPTH or lc.game_state(matrix) != 'not over':
        return evaluate_board(matrix, weights)  # Use the combined heuristic here
    
    if maximizing_player:
        # Max node: player's turn (maximize score)
        best_score = -float('inf')
        for move_key in moves:
            new_matrix, done, points = moves[move_key](matrix)
            if done:
                score = expectimax(new_matrix, weights, depth + 1, False)
                best_score = max(best_score, score)
        return best_score
    
    else:
        # Chance node: AI's turn (expectation over random tiles)
        empty_cells = get_empty_cells(matrix)
        if not empty_cells:
            return evaluate_board(matrix, weights)  # Return heuristic value if no empty cells
        
        total_score = 0
        for cell in empty_cells:
            row, col = cell
            # Test both the '2' and '4' possibilities
            for value in [2, 4]:
                new_matrix = place_random_tile(matrix, row, col, value)
                probability = 0.9 if value == 2 else 0.1  # 90% chance of 2, 10% chance of 4
                total_score += probability * expectimax(new_matrix, weights, depth + 1, True)

        return total_score / len(empty_cells)


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

def evaluate_board(matrix, weights):
    """
    Combines different heuristics to evaluate the board.
    The higher the score, the better the board state.
    """

    corner_weight = weights.get('corner_weight', 0)
    monotonicity_weight = weights.get('monotonicity_weight', 0)
    merging_weight =  weights.get('merging_weight', 0)
    empty_tiles_weight = weights.get('empty_tiles_weight', 0)
    clustering_weight = weights.get('clustering_weight', 0)
    smoothness_weight = weights.get('smoothnes_weights', 0)

    # smoothness_weight = 0.1
    # monotonicity_weight = 1.0
    # empty_cells_weight = 2.7
    # max_tile_weight = 1.0
    
    corner = corner_heuristic(matrix)
    monotonicity = monotonicity_heuristic(matrix)
    merging = merging_heuristic(matrix)
    empty_cells = count_empty_spaces(matrix)
    clustering = clustering_heuristic(matrix)
    smoothness = smoothness_heuristic(matrix)

    # smoothness = calculate_smoothness(matrix)
    # monotonicity = calculate_monotonicity(matrix)
    # empty_cells = len(get_empty_cells(matrix))
    # max_tile = max(max(row) for row in matrix)

    # Weighted sum of different heuristics
    return (corner_weight * corner +
            monotonicity_weight * monotonicity +
            merging_weight * merging +
            empty_tiles_weight * empty_cells +
            clustering_weight * clustering +
            smoothness_weight * smoothness)



