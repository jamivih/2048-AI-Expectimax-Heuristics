'''
First part: (1 points)
(evaluation of this part is based on the performance of this heuristic algorithm of yours, how well you explain what your heuristics are and how well you have tested the results for your algorithm)
- [DONE] add heuristic rules for the program to play the game
- [DONE] run simulation results over 100 runs for each of your heuristics/combination of heuristics

Second part: (2 points)
(evaluation of this part is based on how well you have implemented the expectimax algorithm, how well you can explain how the algorithm works and how well you have tested the results that you can obtain with your algorithm)
- implement so called expectimax algorithm to handle chances included in the game
- combine your heuristics and the expectimax algorithms to work together
- run simulations over 100 runs to show how well your AI implementation Works
- report the results over 100 runs of your algorithm for the game

Main changes must be done to the files AI_heuristics.py, AI_minimax.py and AI_both.py.
'''

# import AI_heuristics as AI
import AI_both2 as AI
import logic
import constants as c
import numpy as np
import itertools



def run_simulation(weights, num_runs=2):
    total_points = 0
    all_points = []
    progress = 0
    losses = 0
    for i in range(num_runs):
        matrix = logic.new_game(c.GRID_LEN)  # Initialize a new game

        game_over = False
        points = 0

        moves = {
            'Up': logic.up,
            'Down': logic.down,
            'Left': logic.left,
            'Right': logic.right
        }
        while not game_over:
            move = AI.AI_play(matrix, weights)  # Pass weights to AI_play
            if move is None:
                break

            # Execute the move using the dictionary from AI_play
            new_matrix, done, move_points = moves[move](matrix)  # Retrieve points from the move
            points += move_points  # Accumulate points for this run

            if done:
                matrix = logic.add_two(new_matrix)
            else:
                game_over = True  # No valid moves, game over
            game_state = logic.game_state(matrix)
            if game_state == 'lose':
                game_over = True
                losses += 1
        
        total_points += points  # Accumulate points from the game
        all_points.append(points)
        # Progress of the loop in percentages
        progress = i / num_runs * 100
        print(f'\rProgress: {int(progress)}%', end='', flush=True)

    print(f'\n{num_runs} runs best score: {max(all_points)}')
    print(f'lowest score: {min(all_points)}')
    print(f'mean: {np.mean(all_points)}')
    print(f'wins: {num_runs - losses}')
    print(f'losses: {losses}')
    return (total_points / num_runs) # Average points across all simulations


def test_weights():
    # Define ranges for each heuristic
    corner_weights = [0.3, 0.5, 0.8]
    monotonicity_weights = [0.5, 0.8, 1, 1.1, 1.2]
    merging_weights = [0.5, 0.8, 1, 1.1, 1.2]
    empty_tiles_weights = [0.5, 0.8, 1, 1.1]
    clustering_weights = [0.0, 0.2]
    smoothness_weights = [0.0, 0.2]

    # Create all combinations of these weights
    weight_combinations = list(itertools.product(corner_weights, monotonicity_weights, merging_weights, 
                                                empty_tiles_weights, clustering_weights, smoothness_weights))

    # Run the simulations for each combination
    for weights in weight_combinations:
        weight_dict = {
            'corner_weight': weights[0],
            'monotonicity_weight': weights[1],
            'merging_weight': weights[2],
            'empty_tiles_weight': weights[3],
            'clustering_weight': weights[4],
            'smoothness_weights': weights[5]
        }
        avg_score = run_simulation(weight_dict)  # Use your existing run_simulation function
        print(f"Weights: {weight_dict}, Avg Score: {avg_score}")

if __name__ == "__main__":
    test_weights()