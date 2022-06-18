import random
from typing import Dict, List, Tuple

from game_mechanics import (Cell, 
                            WildTictactoeMechanics, 
                            load_dictionary, 
                            render, 
                            save_dictionary)

TEAM_NAME = "TEAM NAME"  # <---- Enter your team name here!


def train(game: WildTictactoeMechanics) -> Dict:
    """
    TODO: Write this function to train your algorithm.

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
                     "p    layer_move": the player to take the next move

    Returns:
    ----
    A value function dictionary to be used by your agent 
    during gameplay. 
    You can structure this however you like - you write 
    the choose_move function that uses it.
    """
    raise NotImplementedError()



def choose_move(board: List[str], value_function: Dict) -> Tuple[int, str]:
    """
    TODO: Write this function
    
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
    ## We provide an example here that chooses a random position 
    ## on the board and places a random counter there.
    
    # position = random.choice([count for count, item in enumerate(board) if item == Cell.EMPTY])
    # counter = random.choice([Cell.O, Cell.X])
    # return position, counter
    raise NotImplementedError()


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

    print(f"{info['winner']} wins!")

    

if __name__ == "__main__":

    ## Example workflow, feel free to add caching if it helps! ###
    my_value_fn = train(WildTictactoeMechanics())
    save_dictionary(my_value_fn, TEAM_NAME)
    my_value_fn = load_dictionary(TEAM_NAME)
    test(WildTictactoeMechanics(), my_value_fn)
    render(choose_move, my_value_fn)
