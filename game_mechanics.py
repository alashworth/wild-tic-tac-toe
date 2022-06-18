import pickle
import random
from typing import Callable, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pygame

######## Below are classes you will use to implement your wild-tic-tac-toe AI ######
class Cell:
    '''
    You will need to interact with this! 
    
    This class represents the state of a single square of the
    tic-tac-toe board.
    
    An X counter is represented by Cell.X
    An O counter is represented by Cell.O
    A blank square represented by Cell.EMPTY
        '''
    EMPTY = " "
    X = "X"
    O = "O"

class Player:
    '''
    Defines which player's turn it is.
    
    Player 1's turn is represented by Player.Player1
    Player 2's turn is represented by Player.Player2
    '''
    Player1 = "Player1"
    Player2 = "Player2"


class WildTictactoeMechanics:
    """
    Env class you interact with to play Wild Tic-Tac-Toe

    Contains the .step() and .reset() functions to run the game. See README.md
        for more details.
    """
    
    def __init__(self):
        self.player_move = random.choice([Player.Player1, Player.Player2])
        self.done = False
        self.board = [
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
        ]

    def step(
        self, position: int, counter: str, verbose: bool = False
    ) -> Tuple[List[str], Optional[float], bool, Dict]:
        """
        Makes 1 step corresponding to 1 player playing 1 counter.

        Returns the new board, reward, whether the game is done.
        """
        assert not self.done, "Game is done. Call reset() before taking further steps."

        row, col = convert_to_indices(position)
        assert (
            self.board[row][col] == Cell.EMPTY
        ), "You moved onto a square that already has a counter on it!"

        self.mark_square(row, col, counter)
        if verbose:
            print(self)

        winner = self._check_winner()
        reward: Optional[float] = None  # fucking mypy

        if winner is not None:
            self.done = True
            winner = self.player_move
            reward = 1.0
            if verbose:
                print(f"{self.player_move.value} wins!")
        elif self.is_board_full():
            self.done = True
            reward = 0.0
            if verbose:
                print("Game Drawn")
        else:
            reward = None

        self.switch_player()
        info = {"player_move": self.player_move if not self.done else None, "winner": winner}

        return flatten_board(self.board), reward, self.done, info

    def reset(self) -> Tuple[List[str], Optional[float], bool, Dict]:
        self.board = [
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
        ]

        self.player_move = random.choice([Player.Player1, Player.Player2])
        self.done = False
        return flatten_board(self.board), None, self.done, {"player_move": self.player_move}
    
    def mark_square(self, row: int, col: int, counter: str):
        self.board[row][col] = counter

    def __repr__(self):
        return str(np.array([x.value for xs in self.board for x in xs]).reshape((3, 3))) + "\n"

    def is_board_full(self):
        """Check if the board is full by checking for empty cells after flattening board."""
        return all(c != Cell.EMPTY for c in [i for sublist in self.board for i in sublist])

    def update(self, move: Tuple[int, int], piece: str) -> None:
        self.mark_square(move[0], move[1], piece)

    def _check_winning_set(self, iterable: Iterable[Cell]) -> bool:
        unique_pieces = set(iterable)
        return Cell.EMPTY not in unique_pieces and len(unique_pieces) == 1

    def _check_winner(self) -> Optional[Cell]:
        # Check rows
        for row in self.board:
            if self._check_winning_set(row):
                return row[0]

        # Check columns
        for column in [*zip(*self.board)]:
            if self._check_winning_set(column):
                return column[0]

        # Check major diagonal
        size = len(self.board)
        major_diagonal = [self.board[i][i] for i in range(size)]
        if self._check_winning_set(major_diagonal):
            return major_diagonal[0]

        # Check minor diagonal
        minor_diagonal = [self.board[i][size - i - 1] for i in range(size)]
        if self._check_winning_set(minor_diagonal):
            return minor_diagonal[0]

        return None

    def switch_player(self) -> None:
        self.player_move = Player.Player1 if self.player_move == Player.Player2 else Player.Player2





######## Do not worry about anything below here ###################


WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

RED = (255, 0, 0)
BG_COLOR = (20, 200, 160)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)




def flatten_board(board: List[str]) -> List[str]:
    return [x for xs in board for x in xs]


def save_dictionary(my_dict: Dict, team_name: str) -> None:
    file_name = f"dict_{team_name}.pkl"
    with open(file_name, "wb") as f:
        pickle.dump(my_dict, f)


def load_dictionary(team_name: str) -> Dict:
    file_name = f"dict_{team_name}.pkl"
    with open(file_name, "rb") as f:
        return pickle.load(f)


def draw_non_board_elements(screen, game, player_move):
    draw_pieces(screen, game, player_move)


PLAYER_COLORS = {
    "Player1": "blue",
    "Player2": "red"
}

counter_colors = {}
def draw_pieces(screen, game, player_move):
    # Draw circles and crosses based on board state
    global counter_colors
    if flatten_board(game.board).count(" ") == 9:
        counter_colors = {}
    
    team_color = PLAYER_COLORS[player_move]


    board = game.board

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            color = counter_colors.get((row, col), team_color)
            if board[row][col] == Cell.O:
                counter_colors[(row, col)] = color
                pygame.draw.circle(
                    screen,
                    color,
                    (
                        int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                        int(row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    ),
                    CIRCLE_RADIUS,
                    CIRCLE_WIDTH,
                )
            elif board[row][col] == Cell.X:
                counter_colors[(row, col)] = color
                pygame.draw.line(
                    screen,
                    color,
                    (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                    (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                    CROSS_WIDTH,
                )
                pygame.draw.line(
                    screen,
                    color,
                    (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                    (
                        col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                        row * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                    ),
                    CROSS_WIDTH,
                )


def check_and_draw_win(board: List, counter: str, screen: pygame.Surface, player_move: str) -> bool:

    for col in range(BOARD_COLS):
        if board[0][col] == counter and board[1][col] == counter and board[2][col] == counter:
            draw_vertical_winning_line(screen, col, counter, player_move)
            return True

    for row in range(BOARD_ROWS):
        if board[row][0] == counter and board[row][1] == counter and board[row][2] == counter:
            draw_horizontal_winning_line(screen, row, counter, player_move)
            return True

    if board[2][0] == counter and board[1][1] == counter and board[0][2] == counter:
        draw_asc_diagonal(screen, counter, player_move)
        return True

    if board[0][0] == counter and board[1][1] == counter and board[2][2] == counter:
        draw_desc_diagonal(screen, counter, player_move)
        return True

    return False


def draw_vertical_winning_line(screen, col, counter: str, player_move):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    team_color = PLAYER_COLORS[player_move]

    pygame.draw.line(
        screen,
        team_color,
        (posX, 15),
        (posX, HEIGHT - 15),
        LINE_WIDTH,
    )


def draw_horizontal_winning_line(screen, row, counter, player_move):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2

    team_color = PLAYER_COLORS[player_move]
    pygame.draw.line(
        screen,
        team_color,
        (15, posY),
        (WIDTH - 15, posY),
        WIN_LINE_WIDTH,
    )


def draw_asc_diagonal(screen, counter: str, player_move):
    team_color = PLAYER_COLORS[player_move]
    pygame.draw.line(
        screen,
        team_color,
        (15, HEIGHT - 15),
        (WIDTH - 15, 15),
        WIN_LINE_WIDTH,
    )


def draw_desc_diagonal(screen, counter: str, player_move):
    team_color = PLAYER_COLORS[player_move]
    pygame.draw.line(
        screen,
        team_color,
        (15, 15),
        (WIDTH - 15, HEIGHT - 15),
        WIN_LINE_WIDTH,
    )


def convert_to_indices(number: int) -> Tuple[int, int]:
    assert number in range(9), f"Output ({number}) not a valid number from 0 -> 8"
    return number // 3, number % 3

def robot_choose_move(board: List[Cell]) -> Tuple[int, Cell]:
    position: int = random.choice([count for count, item in enumerate(board) if item == Cell.EMPTY])
    counter: Cell = random.choice([Cell.O, Cell.X])
    return position, counter

def render(
    choose_move: Callable[[List[str], Dict], Tuple],
    player_dict: Dict,
):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TIC TAC TOE")
    screen.fill(BG_COLOR)

    # DRAW LINES
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(
        screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH
    )

    game = WildTictactoeMechanics()

    game_quit = False
    game_over = False
    player_move = random.choice([Player.Player1, Player.Player2])

    while not game_quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and game_over):
                game_quit = True

            if event.type == pygame.MOUSEBUTTONDOWN and not game_quit:

                if player_move == Player.Player1:
                    pos, counter = choose_move(flatten_board(game.board), player_dict)
                elif player_move == Player.Player2:
                    pos, counter = robot_choose_move(flatten_board(game.board))

                row, col = convert_to_indices(pos)
                assert game.board[row][col] == Cell.EMPTY
                game.mark_square(row, col, counter)

                game_over = check_and_draw_win(
                    game.board, Cell.X, screen=screen, player_move=player_move
                ) or check_and_draw_win(game.board, Cell.O, screen=screen, player_move=player_move)
                if game_over:
                    print(f"{player_move} won!")
                draw_non_board_elements(screen, game, player_move)
                player_move = Player.Player1 if player_move == Player.Player2 else Player.Player2


        pygame.display.update()
