import random
from typing import Dict, List, Tuple, NewType, Set
import doctest

from game_mechanics import (Cell,
	convert_to_indices, Player, WildTictactoeMechanics,
	load_dictionary,
	render,
	save_dictionary)

TEAM_NAME = "SCORPIONS"  # <---- Enter your team name here!

import itertools as it
import numpy as np
from collections import defaultdict
import operator
import copy

def valid_moves(board) -> List[Tuple[int, str]]:
	"""Return valid moves from a given position.

	>>> valid_moves(["O", "X", "O", "X", "O", "X", "X", "O", " "])
	[(8, 'O'), (8, 'X')]
	"""
	empty_positions = [count for count, item in enumerate(board) if item == Cell.EMPTY]
	actions = sorted([(x, y) for y in [Cell.O, Cell.X] for x in empty_positions])
	return actions

def random_policy(board) -> Tuple[int, str]:
	position, counter = random.choice(valid_moves(board))
	return position, counter

def copy_board(board: WildTictactoeMechanics):
	env = WildTictactoeMechanics()
	env.board = copy.deepcopy(board.board)
	env.player_move = board.player_move
	env.done = board.done
	return env

def train(game: WildTictactoeMechanics) -> Dict:
	"""
	Arg:
	----
	game  The Env that you interact with to play Wild Tic-Tac-Toe.
	It has two useful functions: .step() & .reset()
		.reset(): starts a new game with a clean board and
				  randomly chosen first player

		.step():  Make a move on the current board.
				  This function takes three arguments:
				  position & counter (see choose_move() for
				  more details) and verbose - whether to
				  print the state of the board after each
				  move. It returns a tuple of length 4
				  (see 'Variables' below).

	Variables:
	----
	Both reset and step return the same 4 variables:
		observation (List[int]): The state of the board as a
								 list of ints (see choose_move)
		reward [1, 0 or None]: The reward from the environment
							   after the current move.
							   1 = win, 0 = draw/lose,
							   None = no winner on this turn
		done (bool): True if the game is over, False otherwise.
		info (dict): Additional information about the current
					 state of the game.
					 "winner": winner of the game, if there is one.
					 "player_move": the player to take the next move

	Returns:
	----
	A value function dictionary to be used by your agent
	during gameplay.
	You can structure this however you like - you write
	the choose_move function that uses it.
	"""

	value_function = defaultdict(float)
	delta = 1000
	threshold = 0.001
	n_iters = 0
	states_explored = 0
	states = it.product([Cell.X, Cell.O, Cell.EMPTY], repeat=9)
	while delta > threshold:
		delta = 0
		for s in states:
			# initialize s
			env = WildTictactoeMechanics()
			invalid_board = False
			for i, c in enumerate(s):
				state, reward, done, info = env.step(i, c)
				if done:
					invalid_board = True
					break
			if invalid_board:
				continue

			v = value_function[tuple(s)]
			max_action = np.NINF
			for position, marker in valid_moves(s):
				bcpy = copy_board(env)
				next_state, reward, done, info = bcpy.step(position, marker)
				if reward is None:
					reward = -0.04
				update = reward + value_function[tuple(next_state)]
				max_action = max(max_action, update)
			value_function[tuple(s)] = max_action
			delta = max(delta, abs(v - max_action))
		n_iters += 1
		print(f"num iter: {n_iters}")
	return value_function


def choose_move(board: List[str], value_function: Dict) -> Tuple[int, str]:
	"""
	This is what will be called during competitive play.

	It takes the current state of the board and value function
	dictionary as input and returns a single move to play.

	Args:
		board: list representing the board.
				(see README Technical Details for more info)

		value_function: The dictionary output by train().

	Returns:
		position (int): The position you want to place your piece
						in (an integer 0 -> 8), where 0 is the top
						left square and 8 is the bottom right.
		counter (str): The counter you want to place your piece.
					   Either "X" or "O".

	It's important to think about exactly what this function
	does. It will choose your moves in the competition!
	"""
	actions = valid_moves(board)
	best_action = (None, None)
	best_utility = np.NINF
	for position, marker in actions:
		b = board.copy()
		b[position] = marker
		util = value_function[tuple(b)]
		if util > best_utility:
			best_action = (position, marker)
			best_utility = util
	return best_action


def test(game, my_value_fn: Dict):
	"""Test your algorithm here!

	Args:
		game: a WildTicTacToeMechanics object.
		my_value_fn (Dict): the dictionary returned from your
							 training function.
	"""

	# The example below plays a single game of wild tictactoe
	# against itself, think about how you might want to adapt this
	# to test the performance of your algorithm.
	observation, reward, done, info = game.reset()
	while not done:
		next_position, next_counter = choose_move(observation, my_value_fn)
		observation, reward, done, info = game.step(next_position, next_counter, verbose=False)

	#(f"{info['winner']} wins!")
	if info['winner'] == "Player1":
		return 1
	else:
		return -1


if __name__ == "__main__":
	pass
	my_value_fn = train(WildTictactoeMechanics())
	save_dictionary(my_value_fn, TEAM_NAME)
	my_value_fn = load_dictionary(TEAM_NAME)
	net_wins = 0
	for _ in range(100000):
		net_wins += test(WildTictactoeMechanics(), my_value_fn)
	print(f"Net wins out of 100k: {net_wins}")
	render(choose_move, my_value_fn)
