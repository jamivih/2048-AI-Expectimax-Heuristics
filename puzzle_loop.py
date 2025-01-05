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


def run_simulation(weights, num_runs=100):
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

    print(f'\n{num_runs} runs highest score: {max(all_points)}')
    print(f'lowest score: {min(all_points)}')
    print(f'mean: {np.mean(all_points)}')
    print(f'wins: {num_runs - losses}')
    print(f'losses: {losses}')
    return (total_points / num_runs) # Average points across all simulations


def test_weights():
    weights = {
        'corner_weight': .5,
        'monotonicity_weight': 1.2,
        'merging_weight': 1.2,
        'empty_tiles_weight': 0.5,
        'clustering_weight': 0,
        'smoothness_weights': 0
    } 
 
    run_simulation(weights)

if __name__ == "__main__":
    test_weights()