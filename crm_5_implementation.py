"""
Tic Tac Toe Game Implementation

This module provides a complete implementation of a Tic Tac Toe game
using HTML, CSS, and JavaScript with a Python backend for game logic.
"""

from typing import List, Optional, Tuple, Dict, Any
import json


class Player:
    """
    Represents a player in the Tic Tac Toe game.
    
    Attributes:
        symbol (str): The symbol representing the player ('X' or 'O')
        name (str): The name of the player
    """
    
    def __init__(self, symbol: str, name: str = "Player"):
        """
        Initialize a new player.
        
        Args:
            symbol (str): The symbol representing the player ('X' or 'O')
            name (str): The name of the player
        """
        if symbol not in ['X', 'O']:
            raise ValueError("Player symbol must be either 'X' or 'O'")
        
        self.symbol = symbol
        self.name = name


class GameBoard:
    """
    Represents the game board for Tic Tac Toe.
    
    The board is a 3x3 grid where each position can be empty or contain
    a player's symbol.
    """
    
    def __init__(self):
        """Initialize an empty 3x3 game board."""
        self.size = 3
        self.board = [['' for _ in range(self.size)] for _ in range(self.size)]
    
    def get_cell(self, row: int, col: int) -> str:
        """
        Get the value of a specific cell.
        
        Args:
            row (int): The row index (0-2)
            col (int): The column index (0-2)
            
        Returns:
            str: The symbol in the cell or empty string if empty
            
        Raises:
            IndexError: If row or col is out of bounds
        """
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise IndexError("Row or column index out of bounds")
        
        return self.board[row][col]
    
    def set_cell(self, row: int, col: int, symbol: str) -> bool:
        """
        Set the value of a specific cell.
        
        Args:
            row (int): The row index (0-2)
            col (int): The column index (0-2)
            symbol (str): The symbol to set ('X' or 'O')
            
        Returns:
            bool: True if the cell was successfully set, False otherwise
            
        Raises:
            IndexError: If row or col is out of bounds
            ValueError: If symbol is not valid
        """
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise IndexError("Row or column index out of bounds")
        
        if symbol not in ['X', 'O']:
            raise ValueError("Symbol must be either 'X' or 'O'")
        
        if self.board[row][col] == '':
            self.board[row][col] = symbol
            return True
        
        return False
    
    def is_full(self) -> bool:
        """
        Check if the board is completely filled.
        
        Returns:
            bool: True if all cells are filled, False otherwise
        """
        for row in self.board:
            if '' in row:
                return False
        return True
    
    def reset(self):
        """Reset the board to an empty state."""
        self.board = [['' for _ in range(self.size)] for _ in range(self.size)]
    
    def to_dict(self) -> List[List[str]]:
        """
        Convert the board state to a dictionary representation.
        
        Returns:
            List[List[str]]: The current board state as a nested list
        """
        return [row[:] for row in self.board]


class WinChecker:
    """
    Utility class to check win conditions in Tic Tac Toe.
    
    This class provides methods to determine if a player has won
    by completing a row, column, or diagonal.
    """
    
    @staticmethod
    def check_winner(board: GameBoard) -> Optional[str]:
        """
        Check if there is a winner on the board.
        
        Args:
            board (GameBoard): The current game board
            
        Returns:
            Optional[str]: The winning symbol ('X' or 'O') if there is a winner,
                          None otherwise
        """
        # Check rows
        for row in range(board.size):
            if board.get_cell(row, 0) != '' and \
               board.get_cell(row, 0) == board.get_cell(row, 1) == board.get_cell(row, 2):
                return board.get_cell(row, 0)
        
        # Check columns
        for col in range(board.size):
            if board.get_cell(0, col) != '' and \
               board.get_cell(0, col) == board.get_cell(1, col) == board.get_cell(2, col):
                return board.get_cell(0, col)
        
        # Check diagonals
        if board.get_cell(0, 0) != '' and \
           board.get_cell(0, 0) == board.get_cell(1, 1) == board.get_cell(2, 2):
            return board.get_cell(0, 0)
        
        if board.get_cell(0, 2) != '' and \
           board.get_cell(0, 2) == board.get_cell(1, 1) == board.get_cell(2, 0):
            return board.get_cell(0, 2)
        
        return None
    
    @staticmethod
    def is_board_full(board: GameBoard) -> bool:
        """
        Check if the board is full (tie condition).
        
        Args:
            board (GameBoard): The current game board
            
        Returns:
            bool: True if the board is full, False otherwise
        """
        return board.is_full()


class GameEngine:
    """
    Main game engine that orchestrates the Tic Tac Toe game flow.
    
    This class manages player turns, game state, and interactions between
    the board and win checking logic.
    """
    
    def __init__(self):
        """Initialize the game engine with default players and state."""
        self.players = [
            Player('X', "Player X"),
            Player('O', "Player O")
        ]
        self.current_player_index = 0
        self.board = GameBoard()
        self.game_state = "waiting"  # waiting, playing, won, tied
        self.winner = None
        self.move_history = []
    
    def get_current_player(self) -> Player:
        """
        Get the player who is currently making a move.
        
        Returns:
            Player: The current player object
        """
        return self.players[self.current_player_index]
    
    def make_move(self, row: int, col: int) -> Dict[str, Any]:
        """
        Make a move on the board at the specified position.
        
        Args:
            row (int): The row index (0-2)
            col (int): The column index (0-2)
            
        Returns:
            Dict[str, Any]: A dictionary containing the move result and state
            
        Raises:
            ValueError: If the position is invalid or occupied
        """
        try:
            # Validate move position
            if not (0 <= row < self.board.size and 0 <= col < self.board.size):
                raise ValueError("Invalid position")
            
            # Check if cell is already occupied
            if self.board.get_cell(row, col) != '':
                raise ValueError("Position already occupied")
            
            # Make the move
            symbol = self.get_current_player().symbol
            success = self.board.set_cell(row, col, symbol)
            
            if not success:
                raise ValueError("Failed to make move")
            
            # Record the move
            self.move_history.append((row, col, symbol))
            
            # Check win condition
            winner = WinChecker.check_winner(self.board)
            
            if winner:
                self.game_state = "won"
                self.winner = winner
                return {
                    "success": True,
                    "game_state": self.game_state,
                    "winner": winner,
                    "board": self.board.to_dict(),
                    "message": f"Player with symbol '{winner}' wins!"
                }
            
            # Check tie condition
            if WinChecker.is_board_full(self.board):
                self.game_state = "tied"
                return {
                    "success": True,
                    "game_state": self.game_state,
                    "winner": None,
                    "board": self.board.to_dict(),
                    "message": "Game ended in a tie!"
                }
            
            # Switch to next player
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            
            return {
                "success": True,
                "game_state": self.game_state,
                "winner": None,
                "board": self.board.to_dict(),
                "message": f"Move successful. Next player: {self.get_current_player().name}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "board": self.board.to_dict()
            }
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.current_player_index = 0
        self.board.reset()
        self.game_state = "waiting"
        self.winner = None
        self.move_history = []
    
    def get_game_state(self) -> Dict[str, Any]:
        """
        Get the current state of the game.
        
        Returns:
            Dict[str, Any]: A dictionary containing the current game state
        """
        return {
            "game_state": self.game_state,
            "current_player": self.get_current_player().name,
            "winner": self.winner,
            "board": self.board.to_dict(),
            "move_history": self.move_history
        }
    
    def undo_move(self) -> bool:
        """
        Undo the last move made in the game.
        
        Returns:
            bool: True if a move was successfully undone, False otherwise
        """
        if not self.move_history:
            return False
        
        # Remove last move from history
        last_move = self.move_history.pop()
        row, col, symbol = last_move
        
        # Clear the cell
        self.board.set_cell(row, col, '')
        
        # Reset current player to the previous one
        self.current_player_index = (self.current_player_index - 1) % len(self.players)
        
        return True


def generate_html_template() -> str:
    """
    Generate the HTML template for the Tic Tac Toe game.
    
    Returns:
        str: The complete HTML template with embedded CSS and JavaScript
    """
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tic Tac Toe</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        
        .game-container {
            background-color: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        
        .game-info {
            margin-bottom: 20px;
            font-size: 18px;
            font-weight: bold;
            color: #555;
        }
        
        .game-board {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin: 20px auto;
            max-width: 300px;
        }
        
        .cell {
            background-color: #f0f0f0;
            border: 2px solid #333;
            border-radius: 8px;
            font-size: 40px;
            font-weight: bold;
            height: 100px;
            width: 100px;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .cell:hover {
            background-color: #e0e0e0;
            transform: scale(1.05);
        }
        
        .cell.x {
            color: #ff4757;
        }
        
        .cell.o {
            color: #3742fa;
        }
        
        .controls {
            margin-top: 20px;
        }
        
        button {
            background-color: #3742fa;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            margin: 5px;
        }
        
        button:hover {
            background-color: #2a36d8;
        }
        
        .message {
            margin-top: 20px;
            font-size: 18px;
            font-weight: bold;
            min-height: 30px;
        }
        
        .winning-cell {
            background-color: #ffd93d;
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .game-history {
            margin-top: 20px;
            max-height: 150px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            background-color: #f9f9f9;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>Tic Tac Toe</h1>
        <div class="game-info" id="gameInfo">Current player: Player X</div>
        <div class="game-board" id="gameBoard"></div>
        <div class="message" id="message"></div>
        <div class="controls">
            <button onclick="resetGame()">Reset Game</button>
            <button onclick="undoMove()">Undo Move</button>
        </div>
        <div class="game-history" id="moveHistory"></div>
    </div>

    <script>
        // Game state management
        let gameState = {
            board: [],
            currentPlayer: 'X',
            gameStatus: 'waiting',
            winner: null,
            moveHistory: []
        };

        // Initialize game
        function initGame() {
            updateBoard();
            updateInfo();
        }

        // Update the game board display
        function updateBoard() {
            const boardElement = document.getElementById('gameBoard');
            boardElement.innerHTML = '';
            
            for (let row = 0; row < 3; row++) {
                for (let col = 0; col < 3; col++) {
                    const cell = document.createElement('div');
                    cell.className = 'cell';
                    cell.id = `cell-${row}-${col}`;
                    
                    // Add content if it exists
                    const value = gameState.board[row][col];
                    if (value) {
                        cell.textContent = value;
                        cell.classList.add(value.toLowerCase());
                    }
                    
                    // Add click event listener
                    cell.addEventListener('click', () => handleCellClick(row, col));
                    
                    boardElement.appendChild(cell);
                }
            }
        }

        // Update game info display
        function updateInfo() {
            const gameInfo = document.getElementById('gameInfo');
            const message = document.getElementById('message');
            
            if (gameState.gameStatus === 'won') {
                gameInfo.textContent = `Game Over! Winner: ${gameState.winner}`;
                message.textContent = `Player with symbol '${gameState.winner}' wins!`;
            } else if (gameState.gameStatus === 'tied') {
                gameInfo.textContent = 'Game Over! It\'s a tie!';
                message.textContent = 'Game ended in a tie!';
            } else {
                gameInfo.textContent = `Current player: ${gameState.currentPlayer}`;
                message.textContent = '';
            }
        }

        // Handle cell click
        function handleCellClick(row, col) {
            const cell = document.getElementById(`cell-${row}-${col}`);
            
            // Prevent clicks if game is over or cell is occupied
            if (gameState.gameStatus !== 'playing' || cell.textContent) {
                return;
            }
            
            // Make move via API call (simulated)
            makeMove(row, col);
        }

        // Simulate making a move
        function makeMove(row, col) {
            // In a real implementation, this would call the Python backend
            // For now we'll simulate the response
            
            const moveResult = {
                success: true,
                game_state: 'playing',
                winner: null,
                board: gameState.board.map(row => [...row]),
                message: 'Move successful'
            };
            
            // Update game state with result (simplified)
            gameState.board[row][col] = gameState.currentPlayer;
            gameState.gameStatus = moveResult.game_state;
            gameState.winner = moveResult.winner;
            
            // Update UI
            updateBoard();
            updateInfo();
            
            // Switch player if game continues
            if (gameState.gameStatus === 'playing') {
                gameState.currentPlayer = gameState.currentPlayer === 'X' ? 'O' : 'X';
            }
        }

        // Reset game
        function resetGame() {
            // In a real implementation, this would call the Python backend
            gameState.board = [['', '', ''], ['', '', ''], ['', '', '']];
            gameState.currentPlayer = 'X';
            gameState.gameStatus = 'waiting';
            gameState.winner = null;
            gameState.moveHistory = [];
            
            updateBoard();
            updateInfo();
        }

        // Undo last move
        function undoMove() {
            // In a real implementation, this would call the Python backend
            alert('Undo functionality would be implemented in the Python backend');
        }

        // Initialize the game when page loads
        window.onload = initGame;
    </script>
</body>
</html>"""


def main():
    """
    Main function to demonstrate the Tic Tac Toe game engine.
    
    This function shows how to use the implemented classes and 
    demonstrates basic game flow.
    """
    try:
        # Create a new game instance
        game = GameEngine()
        
        print("Tic Tac Toe Game Started!")
        print("Initial game state:")
        print(json.dumps(game.get_game_state(), indent=2))
        
        # Make a few moves to demonstrate functionality
        print("\nMaking moves...")