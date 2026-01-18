"""
Tic Tac Toe Game Implementation

This module provides a complete implementation of the Tic Tac Toe game
with HTML, CSS, and JavaScript integration using Python backend.
"""

import json
from typing import List, Optional, Tuple, Dict, Any
from enum import Enum
from dataclasses import dataclass


class Player(Enum):
    """Enumeration representing game players."""
    X = "X"
    O = "O"
    EMPTY = ""


class GameStatus(Enum):
    """Enumeration representing game states."""
    PLAYING = "playing"
    X_WINS = "x_wins"
    O_WINS = "o_wins"
    DRAW = "draw"


@dataclass
class GameMove:
    """Represents a single move in the game."""
    player: Player
    position: int


class TicTacToeGame:
    """
    Main game controller for Tic Tac Toe implementation.
    
    This class manages the game state, player turns, win conditions,
    and provides methods to interact with the game.
    """

    def __init__(self) -> None:
        """Initialize a new Tic Tac Toe game."""
        self.board: List[Player] = [Player.EMPTY] * 9
        self.current_player: Player = Player.X
        self.game_status: GameStatus = GameStatus.PLAYING
        self.move_history: List[GameMove] = []
        self.winning_combinations: List[List[int]] = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]

    def make_move(self, position: int) -> bool:
        """
        Make a move at the specified position.
        
        Args:
            position: The board position (0-8) to make a move
            
        Returns:
            bool: True if the move was successful, False otherwise
            
        Raises:
            ValueError: If position is out of range
        """
        if not 0 <= position <= 8:
            raise ValueError("Position must be between 0 and 8")
            
        if self.board[position] != Player.EMPTY:
            return False
            
        # Make the move
        self.board[position] = self.current_player
        self.move_history.append(GameMove(self.current_player, position))
        
        # Check for win or draw
        self._check_game_end()
        
        # Switch player
        if self.game_status == GameStatus.PLAYING:
            self.current_player = Player.O if self.current_player == Player.X else Player.X
            
        return True

    def _check_game_end(self) -> None:
        """
        Check if the game has ended (win or draw).
        
        Updates the game_status based on current board state.
        """
        # Check for win
        for combination in self.winning_combinations:
            if (self.board[combination[0]] == self.board[combination[1]] == 
                self.board[combination[2]] != Player.EMPTY):
                if self.board[combination[0]] == Player.X:
                    self.game_status = GameStatus.X_WINS
                else:
                    self.game_status = GameStatus.O_WINS
                return
                
        # Check for draw
        if all(cell != Player.EMPTY for cell in self.board):
            self.game_status = GameStatus.DRAW

    def get_board_state(self) -> List[str]:
        """
        Get the current board state as strings.
        
        Returns:
            List[str]: Current board state with player symbols or empty strings
        """
        return [cell.value for cell in self.board]

    def get_game_state(self) -> Dict[str, Any]:
        """
        Get complete game state for serialization.
        
        Returns:
            Dict[str, Any]: Complete game state dictionary
        """
        return {
            "board": self.get_board_state(),
            "current_player": self.current_player.value,
            "game_status": self.game_status.value,
            "move_history": [
                {
                    "player": move.player.value,
                    "position": move.position
                } for move in self.move_history
            ]
        }

    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.board = [Player.EMPTY] * 9
        self.current_player = Player.X
        self.game_status = GameStatus.PLAYING
        self.move_history = []

    def get_winner(self) -> Optional[Player]:
        """
        Get the winner of the game if there is one.
        
        Returns:
            Optional[Player]: The winning player or None if no winner
        """
        if self.game_status == GameStatus.X_WINS:
            return Player.X
        elif self.game_status == GameStatus.O_WINS:
            return Player.O
        return None

    def is_game_over(self) -> bool:
        """
        Check if the game has ended.
        
        Returns:
            bool: True if game is over, False otherwise
        """
        return self.game_status != GameStatus.PLAYING

    def get_available_moves(self) -> List[int]:
        """
        Get list of available moves.
        
        Returns:
            List[int]: List of available board positions (0-8)
        """
        return [i for i in range(9) if self.board[i] == Player.EMPTY]


def generate_html_template() -> str:
    """
    Generate HTML template for the Tic Tac Toe game.
    
    Returns:
        str: Complete HTML structure with embedded CSS and JavaScript
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
        }
        
        .game-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            padding: 30px;
            text-align: center;
            max-width: 500px;
            width: 100%;
        }
        
        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }
        
        .status {
            font-size: 1.4em;
            font-weight: bold;
            margin-bottom: 20px;
            padding: 10px;
            border-radius: 8px;
            background-color: #f0f0f0;
        }
        
        .board {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin: 20px auto;
            max-width: 300px;
        }
        
        .cell {
            background: #f8f9fa;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            font-size: 2.5em;
            font-weight: bold;
            height: 100px;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            transition: all 0.3s ease;
            aspect-ratio: 1;
        }
        
        .cell:hover {
            background: #e9ecef;
            transform: scale(1.05);
        }
        
        .cell.x {
            color: #dc3545;
        }
        
        .cell.o {
            color: #007bff;
        }
        
        .controls {
            margin-top: 20px;
        }
        
        button {
            background: #28a745;
            color: white;
            border: none;
            padding: 12px 25px;
            font-size: 1.1em;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s ease;
            margin: 5px;
        }
        
        button:hover {
            background: #218838;
        }
        
        .winning-cell {
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .message {
            font-size: 1.2em;
            margin: 15px 0;
            padding: 10px;
            border-radius: 8px;
        }
        
        .win-message {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .draw-message {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>Tic Tac Toe</h1>
        <div class="status" id="status">Player X's turn</div>
        
        <div class="board" id="board">
            <div class="cell" data-position="0"></div>
            <div class="cell" data-position="1"></div>
            <div class="cell" data-position="2"></div>
            <div class="cell" data-position="3"></div>
            <div class="cell" data-position="4"></div>
            <div class="cell" data-position="5"></div>
            <div class="cell" data-position="6"></div>
            <div class="cell" data-position="7"></div>
            <div class="cell" data-position="8"></div>
        </div>
        
        <div class="controls">
            <button id="reset-btn">Reset Game</button>
        </div>
    </div>

    <script>
        class TicTacToeGame {
            constructor() {
                this.board = Array(9).fill('');
                this.currentPlayer = 'X';
                this.gameStatus = 'playing';
                this.winningCombinations = [
                    [0, 1, 2], [3, 4, 5], [6, 7, 8],  // Rows
                    [0, 3, 6], [1, 4, 7], [2, 5, 8],  // Columns
                    [0, 4, 8], [2, 4, 6]              // Diagonals
                ];
                
                this.init();
            }
            
            init() {
                this.updateStatus();
                this.setupEventListeners();
            }
            
            setupEventListeners() {
                const cells = document.querySelectorAll('.cell');
                const resetButton = document.getElementById('reset-btn');
                
                cells.forEach(cell => {
                    cell.addEventListener('click', () => {
                        const position = parseInt(cell.dataset.position);
                        this.makeMove(position);
                    });
                });
                
                resetButton.addEventListener('click', () => {
                    this.resetGame();
                });
            }
            
            makeMove(position) {
                if (this.gameStatus !== 'playing' || this.board[position] !== '') {
                    return;
                }
                
                this.board[position] = this.currentPlayer;
                this.updateCell(position, this.currentPlayer);
                
                if (this.checkWin()) {
                    this.gameStatus = this.currentPlayer === 'X' ? 'x_wins' : 'o_wins';
                    this.showWinMessage();
                } else if (this.isDraw()) {
                    this.gameStatus = 'draw';
                    this.showDrawMessage();
                } else {
                    this.currentPlayer = this.currentPlayer === 'X' ? 'O' : 'X';
                    this.updateStatus();
                }
            }
            
            checkWin() {
                return this.winningCombinations.some(combo => {
                    const [a, b, c] = combo;
                    return this.board[a] !== '' && 
                           this.board[a] === this.board[b] === this.board[c];
                });
            }
            
            isDraw() {
                return this.board.every(cell => cell !== '');
            }
            
            updateCell(position, player) {
                const cell = document.querySelector(`.cell[data-position="${position}"]`);
                cell.textContent = player;
                cell.classList.add(player.toLowerCase());
            }
            
            updateStatus() {
                const statusElement = document.getElementById('status');
                if (this.gameStatus === 'playing') {
                    statusElement.textContent = `Player ${this.currentPlayer}'s turn`;
                }
            }
            
            showWinMessage() {
                const statusElement = document.getElementById('status');
                statusElement.textContent = `Player ${this.currentPlayer} wins!`;
                statusElement.classList.add('win-message');
                
                this.highlightWinningCells();
            }
            
            highlightWinningCells() {
                const winningCombo = this.winningCombinations.find(combo => {
                    const [a, b, c] = combo;
                    return this.board[a] !== '' && 
                           this.board[a] === this.board[b] === this.board[c];
                });
                
                if (winningCombo) {
                    winningCombo.forEach(position => {
                        const cell = document.querySelector(`.cell[data-position="${position}"]`);
                        cell.classList.add('winning-cell');
                    });
                }
            }
            
            showDrawMessage() {
                const statusElement = document.getElementById('status');
                statusElement.textContent = "It's a draw!";
                statusElement.classList.add('draw-message');
            }
            
            resetGame() {
                this.board = Array(9).fill('');
                this.currentPlayer = 'X';
                this.gameStatus = 'playing';
                
                const cells = document.querySelectorAll('.cell');
                cells.forEach(cell => {
                    cell.textContent = '';
                    cell.classList.remove('x', 'o', 'winning-cell');
                });
                
                const statusElement = document.getElementById('status');
                statusElement.textContent = "Player X's turn";
                statusElement.classList.remove('win-message', 'draw-message');
            }
        }
        
        // Initialize game when DOM is loaded
        document.addEventListener('DOMContentLoaded', () => {
            new TicTacToeGame();
        });
    </script>
</body>
</html>"""


def create_tic_tac_toe_html_file(filename: str = "tic_tac_toe.html") -> None:
    """
    Create a complete HTML file with Tic Tac Toe game.
    
    Args:
        filename: The name of the output HTML file (default: "tic_tac_toe.html")
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(generate_html_template())
        print(f"Successfully created {filename}")
    except IOError as e:
        print(f"Error creating HTML file: {e}")


def main() -> None:
    """Main function to demonstrate usage."""
    print("Creating Tic Tac Toe HTML file...")
    
    # Create the game instance
    game = TicTacToeGame()
    
    # Display initial state
    print("Initial game state:")
    print(json.dumps(game.get_game_state(), indent=2))
    
    # Make some moves
    try:
        game.make_move(0)  # X at position 0
        game.make_move(1)  # O at position 1
        game.make_move(4)  # X at position 4
        game.make_move(3)  # O at position 3
        
        print("\nGame state after moves:")
        print(json.dumps(game.get_game_state(), indent=2))
        
        # Create HTML file
        create_tic_tac_toe_html_file("tic_tac_toe.html")
        
    except ValueError as e:
        print(f"Error making move: {e}")


if __name__ == "__main__":
    main()