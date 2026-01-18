"""
Tic Tac Toe Game Implementation

This module provides a complete implementation of a Tic Tac Toe game
with HTML, CSS, and JavaScript components. The game supports player
turns, win detection, and game state persistence.

Classes:
    TicTacToe: Main game class handling game logic and state management
    GameBoard: Represents the game board and its state
    Player: Represents a player in the game

Functions:
    main: Entry point for running the game
"""

import json
import os
from typing import List, Optional, Tuple, Dict, Any
from enum import Enum
from dataclasses import dataclass


class PlayerSymbol(Enum):
    """Enumeration for player symbols."""
    X = "X"
    O = "O"


class GameStatus(Enum):
    """Enumeration for game status states."""
    PLAYING = "playing"
    X_WINS = "x_wins"
    O_WINS = "o_wins"
    DRAW = "draw"


@dataclass
class Player:
    """Represents a player in the Tic Tac Toe game."""
    symbol: PlayerSymbol
    name: str


class GameBoard:
    """Represents the game board and its state."""
    
    def __init__(self, size: int = 3):
        """
        Initialize the game board.
        
        Args:
            size: The size of the board (default 3 for 3x3)
        """
        self.size = size
        self.board: List[List[Optional[PlayerSymbol]]] = [
            [None for _ in range(size)] for _ in range(size)
        ]
        
    def make_move(self, row: int, col: int, symbol: PlayerSymbol) -> bool:
        """
        Make a move on the board.
        
        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            symbol: Player symbol to place
            
        Returns:
            True if move was successful, False otherwise
            
        Raises:
            IndexError: If row or column is out of bounds
        """
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise IndexError("Move coordinates are out of bounds")
            
        if self.board[row][col] is not None:
            return False
            
        self.board[row][col] = symbol
        return True
        
    def get_cell(self, row: int, col: int) -> Optional[PlayerSymbol]:
        """
        Get the symbol at a specific cell.
        
        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            
        Returns:
            The symbol at the cell or None if empty
        """
        return self.board[row][col]
        
    def is_full(self) -> bool:
        """
        Check if the board is completely filled.
        
        Returns:
            True if board is full, False otherwise
        """
        for row in self.board:
            for cell in row:
                if cell is None:
                    return False
        return True
        
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """
        Get list of all empty cells on the board.
        
        Returns:
            List of tuples containing (row, col) of empty cells
        """
        empty_cells = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] is None:
                    empty_cells.append((row, col))
        return empty_cells
        
    def reset(self) -> None:
        """Reset the board to initial state."""
        self.board = [
            [None for _ in range(self.size)] for _ in range(self.size)
        ]


class TicTacToe:
    """Main game class handling game logic and state management."""
    
    def __init__(self, player1: Player, player2: Player, board_size: int = 3):
        """
        Initialize the Tic Tac Toe game.
        
        Args:
            player1: First player
            player2: Second player
            board_size: Size of the game board (default 3)
        """
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.board = GameBoard(board_size)
        self.status = GameStatus.PLAYING
        self.winner: Optional[Player] = None
        self.move_history: List[Tuple[int, int, PlayerSymbol]] = []
        
    def make_move(self, row: int, col: int) -> bool:
        """
        Make a move for the current player.
        
        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            
        Returns:
            True if move was successful, False otherwise
            
        Raises:
            ValueError: If the game has already ended
        """
        if self.status != GameStatus.PLAYING:
            raise ValueError("Game has already ended")
            
        success = self.board.make_move(row, col, self.current_player.symbol)
        
        if success:
            # Record the move
            self.move_history.append((row, col, self.current_player.symbol))
            
            # Check win condition
            if self._check_win(row, col):
                self.status = GameStatus.X_WINS if self.current_player.symbol == PlayerSymbol.X else GameStatus.O_WINS
                self.winner = self.current_player
            elif self.board.is_full():
                self.status = GameStatus.DRAW
                
            # Switch player
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
            
        return success
        
    def _check_win(self, row: int, col: int) -> bool:
        """
        Check if the last move resulted in a win.
        
        Args:
            row: Last move row
            col: Last move column
            
        Returns:
            True if the move resulted in a win, False otherwise
        """
        symbol = self.board.get_cell(row, col)
        
        # Check row
        if all(self.board.get_cell(row, c) == symbol for c in range(self.board.size)):
            return True
            
        # Check column
        if all(self.board.get_cell(r, col) == symbol for r in range(self.board.size)):
            return True
            
        # Check diagonals
        if row == col:
            # Main diagonal
            if all(self.board.get_cell(i, i) == symbol for i in range(self.board.size)):
                return True
                
        if row + col == self.board.size - 1:
            # Anti-diagonal
            if all(self.board.get_cell(i, self.board.size - 1 - i) == symbol for i in range(self.board.size)):
                return True
                
        return False
        
    def get_game_state(self) -> Dict[str, Any]:
        """
        Get the current game state.
        
        Returns:
            Dictionary containing game state information
        """
        return {
            "status": self.status.value,
            "current_player_symbol": self.current_player.symbol.value,
            "board": [
                [cell.value if cell else None for cell in row]
                for row in self.board.board
            ],
            "winner": self.winner.symbol.value if self.winner else None,
            "move_history": self.move_history
        }
        
    def reset(self) -> None:
        """Reset the game to initial state."""
        self.board.reset()
        self.status = GameStatus.PLAYING
        self.winner = None
        self.current_player = self.player1
        self.move_history.clear()
        
    def get_winner(self) -> Optional[Player]:
        """
        Get the winner of the game.
        
        Returns:
            The winning player or None if no winner
        """
        return self.winner
        
    def get_current_player(self) -> Player:
        """
        Get the current player.
        
        Returns:
            The current player
        """
        return self.current_player
        
    def get_board(self) -> GameBoard:
        """
        Get the game board.
        
        Returns:
            The game board instance
        """
        return self.board


def create_html_template(game_state: Dict[str, Any], game_id: str) -> str:
    """
    Create an HTML template for the Tic Tac Toe game.
    
    Args:
        game_state: Current game state dictionary
        game_id: Unique identifier for the game instance
        
    Returns:
        HTML string representing the game interface
    """
    # Create basic HTML structure with embedded CSS and JavaScript
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tic Tac Toe Game</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        
        .game-container {{
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
            max-width: 500px;
            width: 100%;
        }}
        
        h1 {{
            color: #333;
            margin-bottom: 20px;
        }}
        
        .status {{
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 20px;
            padding: 10px;
            border-radius: 8px;
            background-color: #f0f0f0;
        }}
        
        .board {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin: 20px auto;
            max-width: 300px;
        }}
        
        .cell {{
            aspect-ratio: 1;
            background-color: #f8f9fa;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            font-size: 2em;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: all 0.2s ease;
        }}
        
        .cell:hover {{
            background-color: #e9ecef;
            transform: scale(1.05);
        }}
        
        .cell.x {{
            color: #dc3545;
        }}
        
        .cell.o {{
            color: #007bff;
        }}
        
        .controls {{
            margin-top: 20px;
        }}
        
        button {{
            background-color: #28a745;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 1em;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.2s ease;
            margin: 5px;
        }}
        
        button:hover {{
            background-color: #218838;
        }}
        
        .win-message {{
            color: #28a745;
            font-weight: bold;
            margin-top: 10px;
        }}
        
        .draw-message {{
            color: #ffc107;
            font-weight: bold;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <h1>Tic Tac Toe</h1>
        <div id="status" class="status">Current Player: {game_state['current_player_symbol']}</div>
        <div id="board" class="board">
            {"".join([
                f'<div class="cell" onclick="makeMove({r}, {c})" data-row="{r}" data-col="{c}"></div>'
                for r in range(3) for c in range(3)
            ])}
        </div>
        <div class="controls">
            <button onclick="resetGame()">Reset Game</button>
            <button onclick="saveGame()">Save Game</button>
        </div>
    </div>

    <script>
        const gameState = {json.dumps(game_state)};
        const gameID = "{game_id}";
        
        function updateBoard() {{
            const cells = document.querySelectorAll('.cell');
            const boardState = gameState.board;
            
            cells.forEach((cell, index) => {{
                const row = Math.floor(index / 3);
                const col = index % 3;
                const symbol = boardState[row][col];
                
                if (symbol) {{
                    cell.textContent = symbol;
                    cell.className = `cell ${symbol.toLowerCase()}`;
                }} else {{
                    cell.textContent = '';
                    cell.className = 'cell';
                }}
            }});
            
            updateStatus();
        }}
        
        function updateStatus() {{
            const statusDiv = document.getElementById('status');
            const currentStatus = gameState.status;
            
            if (currentStatus === 'x_wins') {{
                statusDiv.innerHTML = 'Player X Wins!';
                statusDiv.className = 'status win-message';
            }} else if (currentStatus === 'o_wins') {{
                statusDiv.innerHTML = 'Player O Wins!';
                statusDiv.className = 'status win-message';
            }} else if (currentStatus === 'draw') {{
                statusDiv.innerHTML = 'Game is a Draw!';
                statusDiv.className = 'status draw-message';
            }} else {{
                statusDiv.innerHTML = `Current Player: ${{
                    gameState.current_player_symbol
                }}`;
                statusDiv.className = 'status';
            }}
        }}
        
        function makeMove(row, col) {{
            // In a real implementation, this would send the move to the backend
            console.log(`Move made: Row ${row}, Col ${col}`);
        }}
        
        function resetGame() {{
            // In a real implementation, this would reset the game state
            console.log('Game reset requested');
        }}
        
        function saveGame() {{
            // In a real implementation, this would save the game state
            console.log('Game saved');
        }}
        
        // Initialize the board when page loads
        document.addEventListener('DOMContentLoaded', () => {{
            updateBoard();
        }});
    </script>
</body>
</html>
"""
    
    return html_content


def save_game_state(game: TicTacToe, file_path: str) -> None:
    """
    Save the current game state to a JSON file.
    
    Args:
        game: The TicTacToe game instance to save
        file_path: Path to the file where game state should be saved
    """
    try:
        game_state = game.get_game_state()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(game_state, f, indent=2)
            
    except Exception as e:
        raise IOError(f"Failed to save game state: {str(e)}")


def load_game_state(file_path: str) -> Dict[str, Any]:
    """
    Load game state from a JSON file.
    
    Args:
        file_path: Path to the file containing game state
        
    Returns:
        Dictionary containing loaded game state
        
    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Game state file not found: {file_path}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Invalid JSON in game state file", "", 0)


def main() -> None:
    """Main function to demonstrate the Tic Tac Toe game."""
    # Create players
    player1 = Player(PlayerSymbol.X, "Player X")
    player2 = Player(PlayerSymbol.O, "Player O")
    
    # Create game instance
    game = TicTacToe(player1, player2)
    
    # Display initial state
    print("Initial Game State:")
    state = game.get_game_state()
    print(json.dumps(state, indent=2))
    
    # Example moves
    try:
        game.make_move(0, 0)  # X plays at (0,0)
        game.make_move(1, 1)  # O plays at (1,1)
        game.make_move(0, 1)  # X plays at (0,1)
        game.make_move(1, 0)  # O plays at (1,0)
        game.make_move(0, 2)  # X plays at (0,2) - wins
        
        print("\nAfter example moves:")
        state = game.get_game_state()
        print(json.dumps(state, indent=2))
        
        # Save the game state
        save_game_state(game, "games/tic_tac_toe_game.json")
        print("\nGame state saved successfully.")
        
    except Exception as e:
        print(f"Error during game execution: {e}")


if __name__ == "__main__":
    main()
Tic Tac Toe Game Implementation (Clean Version)

Python backend game engine with optional HTML/CSS/JS generation.
"""

from typing import List, Optional, Dict, Any
import json


# -----------------------------
# Player
# -----------------------------
class Player:
    """Represents a Tic Tac Toe player."""

    def __init__(self, symbol: str, name: str):
        if symbol not in ("X", "O"):
            raise ValueError("Symbol must be 'X' or 'O'")
        self.symbol = symbol
        self.name = name


# -----------------------------
# Game Board
# -----------------------------
class GameBoard:
    """3x3 Tic Tac Toe board."""

    def __init__(self):
        self.size = 3
        self.board = [["" for _ in range(3)] for _ in range(3)]

    def get_cell(self, row: int, col: int) -> str:
        self._validate_position(row, col)
        return self.board[row][col]

    def set_cell(self, row: int, col: int, symbol: str) -> None:
        self._validate_position(row, col)

        if symbol not in ("X", "O"):
            raise ValueError("Invalid symbol")

        if self.board[row][col] != "":
            raise ValueError("Cell already occupied")

        self.board[row][col] = symbol

    def clear_cell(self, row: int, col: int) -> None:
        self._validate_position(row, col)
        self.board[row][col] = ""

    def is_full(self) -> bool:
        return all(cell != "" for row in self.board for cell in row)

    def reset(self) -> None:
        self.board = [["" for _ in range(3)] for _ in range(3)]

    def to_dict(self) -> List[List[str]]:
        return [row[:] for row in self.board]

    def _validate_position(self, row: int, col: int) -> None:
        if not (0 <= row < 3 and 0 <= col < 3):
            raise IndexError("Row and column must be between 0 and 2")


# -----------------------------
# Win Checker
# -----------------------------
class WinChecker:
    """Utility class for win checking."""

    @staticmethod
    def check_winner(board: GameBoard) -> Optional[str]:
        b = board.board

        lines = (
            # rows
            b[0], b[1], b[2],
            # columns
            [b[0][0], b[1][0], b[2][0]],
            [b[0][1], b[1][1], b[2][1]],
            [b[0][2], b[1][2], b[2][2]],
            # diagonals
            [b[0][0], b[1][1], b[2][2]],
            [b[0][2], b[1][1], b[2][0]],
        )

        for line in lines:
            if line[0] and line.count(line[0]) == 3:
                return line[0]

        return None


# -----------------------------
# Game Engine
# -----------------------------
class GameEngine:
    """Main Tic Tac Toe game engine."""

    def __init__(self):
        self.players = [
            Player("X", "Player X"),
            Player("O", "Player O"),
        ]
        self.current_player_index = 0
        self.board = GameBoard()
        self.winner: Optional[str] = None
        self.game_over = False
        self.move_history: List[Dict[str, Any]] = []

    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def make_move(self, row: int, col: int) -> Dict[str, Any]:
        if self.game_over:
            return {"success": False, "error": "Game is already over"}

        try:
            symbol = self.current_player().symbol
            self.board.set_cell(row, col, symbol)

            self.move_history.append(
                {"row": row, "col": col, "symbol": symbol}
            )

            winner = WinChecker.check_winner(self.board)
            if winner:
                self.winner = winner
                self.game_over = True
                return self._response(f"{winner} wins!")

            if self.board.is_full():
                self.game_over = True
                return self._response("Game ended in a draw")

            self._switch_player()
            return self._response("Move successful")

        except Exception as e:
            return {"success": False, "error": str(e)}

    def undo_move(self) -> bool:
        if not self.move_history or self.game_over:
            return False

        last = self.move_history.pop()
        self.board.clear_cell(last["row"], last["col"])
        self._switch_player()
        return True

    def reset_game(self) -> None:
        self.board.reset()
        self.current_player_index = 0
        self.winner = None
        self.game_over = False
        self.move_history.clear()

    def get_game_state(self) -> Dict[str, Any]:
        return {
            "board": self.board.to_dict(),
            "current_player": self.current_player().name,
            "winner": self.winner,
            "game_over": self.game_over,
            "moves": self.move_history,
        }

    def _switch_player(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % 2

    def _response(self, message: str) -> Dict[str, Any]:
        return {
            "success": True,
            "message": message,
            "state": self.get_game_state(),
        }


# -----------------------------
# Demo
# -----------------------------
def main() -> None:
    game = GameEngine()
    print("Tic Tac Toe started\n")

    print(json.dumps(game.make_move(0, 0), indent=2))
    print(json.dumps(game.make_move(1, 1), indent=2))
    print(json.dumps(game.make_move(0, 1), indent=2))
    print(json.dumps(game.make_move(2, 2), indent=2))
    print(json.dumps(game.make_move(0, 2), indent=2))  # X wins


if __name__ == "__main__":
    main()
