from typing import List, Dict, Union, Optional
import json

class ConfigManager:
    """
    Singleton class to manage theme configurations for the Tic Tac Toe game.
    Provides a grey-themed color scheme by default.
    """
    _instance = None

    def __new__(cls):
        """
        Ensure only one instance of ConfigManager is created.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_config()
        return cls._instance

    def _init_config(self):
        """
        Initialize default theme configuration with grey color scheme.
        """
        self.theme = {
            'board_bg': '#e0e0e0',          # Light grey background
            'cell_border': '#b0b0b0',       # Medium grey border
            'x_color': '#555555',           # Dark grey for X
            'o_color': '#555555',           # Dark grey for O
            'text_color': '#333333'         # Dark text for readability
        }

    def get_theme(self) -> Dict[str, str]:
        """
        Retrieve the current theme configuration.
        
        Returns:
            Dict[str, str]: Dictionary containing color theme values.
        """
        return self.theme

class Game:
    """
    Core game logic for Tic Tac Toe with grey-themed styling.
    Manages game state, move validation, and win/draw detection.
    """
    def __init__(self):
        """
        Initialize a new game with an empty board and default settings.
        """
        self.board: List[List[str]] = [['' for _ in range(3)] for _ in range(3)]
        self.current_player: str = 'X'
        self.winner: Optional[str] = None
        self.game_over: bool = False
        self.config = ConfigManager().get_theme()

    def make_move(self, row: int, col: int) -> bool:
        """
        Execute a move on the board at the specified position.
        
        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
        
        Returns:
            bool: True if move was successful, False if game is over
        
        Raises:
            ValueError: If row/column is out of bounds or cell is already occupied
        """
        if self.game_over:
            raise ValueError("Game is already over")
        
        if not (0 <= row < 3 and 0 <= col < 3):
            raise ValueError("Row and column must be between 0 and 2")
        
        if self.board[row][col] != '':
            raise ValueError("Cell already occupied")
        
        self.board[row][col] = self.current_player
        self._check_win(row, col)
        self._check_draw()
        
        return True

    def _check_win(self, row: int, col: int) -> None:
        """
        Check if the current move resulted in a win.
        """
        # Check row
        if all(self.board[row][c] == self.current_player for c in range(3)):
            self._set_game_over(self.current_player)
        # Check column
        elif all(self.board[r][col] == self.current_player for r in range(3)):
            self._set_game_over(self.current_player)
        # Check diagonals
        elif row == col and all(self.board[i][i] == self.current_player for i in range(3)):
            self._set_game_over(self.current_player)
        elif row + col == 2 and all(self.board[i][2-i] == self.current_player for i in range(3)):
            self._set_game_over(self.current_player)

    def _check_draw(self) -> None:
        """
        Check if the game is a draw (all cells filled with no winner).
        """
        if all(cell != '' for row in self.board for cell in row):
            self._set_game_over(None)

    def _set_game_over(self, winner: Optional[str]) -> None:
        """
        Set game over status and update winner.
        """
        self.winner = winner
        self.game_over = True

    def get_board(self) -> List[List[str]]:
        """
        Retrieve the current state of the board.
        
        Returns:
            List[List[str]]: 3x3 grid representing the game board
        """
        return [row[:] for row in self.board]

    def get_status(self) -> Dict[str, Union[str, bool]]:
        """
        Retrieve game status information.
        
        Returns:
            Dict[str, Union[str, bool]]: Dictionary containing game state details
        """
        return {
            'winner': self.winner,
            'game_over': self.game_over,
            'current_player': self.current_player,
            'board': self.get_board(),
            'theme': self.config
        }

    def reset_game(self) -> None:
        """
        Reset the game to its initial state.
        """
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False

def main():
    """
    Main function to demonstrate game functionality.
    """
    game = Game()
    print("Initial Board:")
    print(json.dumps(game.get_status(), indent=2))
    
    try:
        game.make_move(0, 0)
        game.make_move(0, 1)
        game.make_move(0, 2)
        print("\nAfter X's win:")
        print(json.dumps(game.get_status(), indent=2))
        
        game.reset_game()
        game.make_move(1, 1)
        game.make_move(0, 0)
        game.make_move(2, 2)
        game.make_move(0, 2)
        game.make_move(2, 0)
        print("\nAfter draw:")
        print(json.dumps(game.get_status(), indent=2))
        
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()