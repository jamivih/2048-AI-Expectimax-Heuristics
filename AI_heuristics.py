import constants as c
import random
import logic

# Mapping keys to the logic functions for movement
commands = {
    'Up': logic.up,
    'Down': logic.down,
    'Left': logic.left,
    'Right': logic.right
}

################### Corner heuristic ###################
'Checks if the largest tile is in one of the corners'
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

def evaluate_move(matrix, weights):
    score = 0

    # Takes weight values from game simulation, default values 0 for bayesian optimization to avoid errors
    corner_weight = weights.get('corner_weight', 0)
    monotonicity_weight =  weights.get('monotonicity_weight', 0)
    merging_weight =  weights.get('merging_weight', 0)
    empty_tiles_weight =  weights.get('empty_tiles_weight', 0)
    clustering =  weights.get('clustering', 0)

    score += corner_weight * corner_heuristic(matrix)
    score += monotonicity_weight * monotonicity_heuristic(matrix)
    score += merging_weight * merging_heuristic(matrix)
    score += empty_tiles_weight * count_empty_spaces(matrix)
    score += clustering * clustering_heuristic(matrix)

    return score
    
def AI_play(matrix, weights):
    moves = {
        'Up': logic.up,
        'Down': logic.down,
        'Left': logic.left,
        'Right': logic.right
    }
    best_move = None
    max_score = -float('inf')

    for move_name, move_func in moves.items():
        new_matrix, done, _ = move_func(matrix)

        if done:
            # Evaluate the move with the given heuristic weights
            future_score = evaluate_move(new_matrix, weights)
            for future_move_name, future_move_func in moves.items():
                future_matrix, future_done, _ = future_move_func(new_matrix)
                if future_done:
                    future_score += evaluate_move(future_matrix, weights) * 0.5

            if future_score > max_score:
                max_score = future_score
                best_move = move_name

    return best_move if best_move is not None else random.choice(['Up', 'Down', 'Left', 'Right'])