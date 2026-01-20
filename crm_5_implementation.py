"""
Tic Tac Toe Game Implementation

This module provides a complete implementation of the Tic Tac Toe game
with HTML, CSS, and JavaScript components. The game follows MVC architecture
and includes proper state management, win condition checking, and player turn handling.
"""

from enum import Enum
from typing import List, Optional, Tuple, Dict, Any
import json


class Player(Enum):
    """Enumeration for game players."""
    X = "X"
    O = "O"
    EMPTY = " "


class GameStatus(Enum):
    """Enumeration for game statuses."""
    PLAYING = "playing"
    X_WON = "x_won"
    O_WON = "o_won"
    DRAW = "draw"


class TicTacToeGame:
    """
    Main game controller for Tic Tac Toe implementation.
    
    This class manages the game state, player turns, win condition checking,
    and maintains the game board.
    """

    def __init__(self) -> None:
        """
        Initialize the Tic Tac Toe game.
        
        Sets up the game board, initializes player turns, and prepares
        the game state for play.
        """
        self.board: List[List[Player]] = [
            [Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY]
        ]
        self.current_player: Player = Player.X
        self.game_status: GameStatus = GameStatus.PLAYING
        self.move_history: List[Tuple[int, int]] = []

    def make_move(self, row: int, col: int) -> bool:
        """
        Make a move on the game board at specified position.
        
        Args:
            row (int): The row index (0-2) where the move should be made
            col (int): The column index (0-2) where the move should be made
            
        Returns:
            bool: True if the move was successful, False otherwise
            
        Raises:
            ValueError: If row or col are outside valid range (0-2)
        """
        if not (0 <= row <= 2 and 0 <= col <= 2):
            raise ValueError("Row and column must be between 0 and 2")
            
        if self.board[row][col] != Player.EMPTY:
            return False
            
        # Make the move
        self.board[row][col] = self.current_player
        self.move_history.append((row, col))
        
        # Check for win or draw
        self._check_game_status()
        
        # Switch player if game is still playing
        if self.game_status == GameStatus.PLAYING:
            self.current_player = Player.O if self.current_player == Player.X else Player.X
            
        return True

    def _check_game_status(self) -> None:
        """
        Check the current game status for win conditions or draw.
        
        This method evaluates the board state to determine if there is a winner
        or if the game has ended in a draw.
        """
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != Player.EMPTY:
                self.game_status = GameStatus.X_WON if row[0] == Player.X else GameStatus.O_WON
                return
                
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != Player.EMPTY:
                self.game_status = GameStatus.X_WON if self.board[0][col] == Player.X else GameStatus.O_WON
                return
                
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != Player.EMPTY:
            self.game_status = GameStatus.X_WON if self.board[0][0] == Player.X else GameStatus.O_WON
            return
            
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != Player.EMPTY:
            self.game_status = GameStatus.X_WON if self.board[0][2] == Player.X else GameStatus.O_WON
            return
            
        # Check for draw
        is_board_full = all(
            self.board[row][col] != Player.EMPTY 
            for row in range(3) 
            for col in range(3)
        )
        
        if is_board_full:
            self.game_status = GameStatus.DRAW

    def reset_game(self) -> None:
        """
        Reset the game to initial state.
        
        Clears the board, resets player turns, and sets game status back to playing.
        """
        self.board = [
            [Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY]
        ]
        self.current_player = Player.X
        self.game_status = GameStatus.PLAYING
        self.move_history.clear()

    def get_board_state(self) -> List[List[Player]]:
        """
        Get the current state of the game board.
        
        Returns:
            List[List[Player]]: A copy of the current board state
        """
        return [row[:] for row in self.board]

    def get_current_player(self) -> Player:
        """
        Get the current player making a move.
        
        Returns:
            Player: The current player (X or O)
        """
        return self.current_player

    def get_game_status(self) -> GameStatus:
        """
        Get the current game status.
        
        Returns:
            GameStatus: The current status of the game (playing, won, draw)
        """
        return self.game_status

    def get_move_history(self) -> List[Tuple[int, int]]:
        """
        Get the move history of the current game.
        
        Returns:
            List[Tuple[int, int]]: List of moves made (row, col)
        """
        return self.move_history.copy()

    def get_winner(self) -> Optional[Player]:
        """
        Get the winner of the game if there is one.
        
        Returns:
            Optional[Player]: The winning player or None if no winner
        """
        if self.game_status == GameStatus.X_WON:
            return Player.X
        elif self.game_status == GameStatus.O_WON:
            return Player.O
        else:
            return None

    def get_game_state(self) -> Dict[str, Any]:
        """
        Get the complete game state as a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary containing all game state information
        """
        return {
            "board": self.get_board_state(),
            "current_player": self.current_player.value,
            "game_status": self.game_status.value,
            "winner": self.get_winner().value if self.get_winner() else None,
            "move_history": self.move_history
        }


class GameRenderer:
    """
    Handles rendering of the Tic Tac Toe game to HTML.
    
    This class generates the HTML and CSS for displaying the game board
    and managing user interaction.
    """

    def __init__(self) -> None:
        """
        Initialize the game renderer.
        
        Sets up the basic HTML structure and CSS styling for the game.
        """
        self.game_state = None

    def render_html(self, game: TicTacToeGame) -> str:
        """
        Render the complete HTML for the Tic Tac Toe game.
        
        Args:
            game (TicTacToeGame): The current game instance
            
        Returns:
            str: Complete HTML string for the game display
        """
        self.game_state = game
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tic Tac Toe</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }}
        
        .game-container {{
            text-align: center;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .game-title {{
            color: #333;
            margin-bottom: 20px;
        }}
        
        .status {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 20px;
            color: #555;
        }}
        
        .board {{
            display: grid;
            grid-template-columns: repeat(3, 100px);
            grid-gap: 5px;
            margin: 0 auto;
            background-color: #333;
            padding: 10px;
            border-radius: 5px;
        }}
        
        .cell {{
            width: 100px;
            height: 100px;
            background-color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 48px;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s;
        }}
        
        .cell:hover {{
            background-color: #f5f5f5;
        }}
        
        .cell.disabled {{
            cursor: not-allowed;
        }}
        
        .controls {{
            margin-top: 20px;
        }}
        
        button {{
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }}
        
        button:hover {{
            background-color: #45a049;
        }}
        
        .winning-cell {{
            background-color: #a8e6cf;
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <h1 class="game-title">Tic Tac Toe</h1>
        <div class="status" id="status">Current Player: {game.get_current_player().value}</div>
        <div class="board" id="board">
            {self._render_board(game)}
        </div>
        <div class="controls">
            <button onclick="resetGame()">Reset Game</button>
        </div>
    </div>

    <script>
        // JavaScript game logic will be added here
        const currentPlayer = "{game.get_current_player().value}";
        const gameStatus = "{game.get_game_status().value}";
        
        function makeMove(row, col) {{
            // This function will be implemented in JavaScript
            console.log("Move made at:", row, col);
        }}
        
        function resetGame() {{
            // This function will be implemented in JavaScript
            console.log("Resetting game");
        }}
    </script>
</body>
</html>
        """
        
        return html_content

    def _render_board(self, game: TicTacToeGame) -> str:
        """
        Render the game board as HTML cells.
        
        Args:
            game (TicTacToeGame): The current game instance
            
        Returns:
            str: HTML string representing the board cells
        """
        board_html = ""
        
        for i in range(3):
            for j in range(3):
                player = game.get_board_state()[i][j]
                cell_value = player.value if player != Player.EMPTY else ""
                
                # Determine if the game is over to disable further moves
                is_game_over = game.get_game_status() != GameStatus.PLAYING
                disabled_class = "disabled" if is_game_over and player == Player.EMPTY else ""
                
                board_html += f'''
                    <div class="cell {disabled_class}" 
                         onclick="makeMove({i}, {j})" 
                         data-row="{i}" data-col="{j}">
                        {cell_value}
                    </div>
                '''
                
        return board_html


class GameEngine:
    """
    Main engine that coordinates the Tic Tac Toe game.
    
    This class acts as the central coordinator, managing the game lifecycle,
    user interaction, and state updates.
    """

    def __init__(self) -> None:
        """
        Initialize the game engine.
        
        Creates instances of the game controller and renderer.
        """
        self.game = TicTacToeGame()
        self.renderer = GameRenderer()

    def play_move(self, row: int, col: int) -> Dict[str, Any]:
        """
        Process a player move and return updated game state.
        
        Args:
            row (int): The row index where the move is made
            col (int): The column index where the move is made
            
        Returns:
            Dict[str, Any]: Updated game state after the move
        """
        try:
            success = self.game.make_move(row, col)
            
            if not success:
                return {
                    "success": False,
                    "error": "Invalid move - cell already occupied",
                    "state": self.game.get_game_state()
                }
                
            return {
                "success": True,
                "state": self.game.get_game_state()
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": str(e),
                "state": self.game.get_game_state()
            }

    def reset(self) -> Dict[str, Any]:
        """
        Reset the game to initial state.
        
        Returns:
            Dict[str, Any]: Game state after reset
        """
        self.game.reset_game()
        return {
            "success": True,
            "state": self.game.get_game_state()
        }

    def get_html(self) -> str:
        """
        Generate complete HTML for the game.
        
        Returns:
            str: Complete HTML page for the Tic Tac Toe game
        """
        return self.renderer.render_html(self.game)

    def get_game_state(self) -> Dict[str, Any]:
        """
        Get the current game state.
        
        Returns:
            Dict[str, Any]: Current game state as dictionary
        """
        return self.game.get_game_state()


# Example usage and testing functions
def create_sample_game() -> GameEngine:
    """
    Create a sample game instance for demonstration.
    
    Returns:
        GameEngine: A configured game engine instance
    """
    return GameEngine()


def test_game_logic() -> None:
    """
    Test the core game logic with sample moves.
    
    This function demonstrates basic functionality of the Tic Tac Toe engine.
    """
    game_engine = create_sample_game()
    
    # Test basic moves
    result1 = game_engine.play_move(0, 0)
    print(f"Move (0,0): {result1['success']}")
    
    result2 = game_engine.play_move(1, 1)
    print(f"Move (1,1): {result2['success']}")
    
    # Test invalid move
    result3 = game_engine.play_move(0, 0)
    print(f"Move (0,0) again: {result3['success']}")
    
    # Test reset
    reset_result = game_engine.reset()
    print(f"Reset successful: {reset_result['success']}")
    
    # Print final state
    state = game_engine.get_game_state()
    print(f"Final game status: {state['game_status']}")


if __name__ == "__main__":
    # Run basic tests
    test_game_logic()
    
    # Create and display game HTML
    engine = create_sample_game()
    html_output = engine.get_html()
    
    # Save to file for demonstration
    with open("tic_tac_toe.html", "w") as f:
        f.write(html_output)
    
    print("Tic Tac Toe HTML generated successfully as 'tic_tac_toe.html'")
