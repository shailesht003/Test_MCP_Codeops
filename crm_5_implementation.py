"""
Tic Tac Toe Game Implementation

This module provides a complete implementation of a Tic Tac Toe game
with HTML, CSS, and JavaScript components.
"""

from typing import List, Optional, Tuple, Dict, Any
import json


class TicTacToeGame:
    """
    A class to represent the Tic Tac Toe game logic.
    
    This class manages the game state, player moves, and win conditions
    according to standard Tic Tac Toe rules.
    """

    def __init__(self) -> None:
        """Initialize a new Tic Tac Toe game."""
        self.board: List[str] = [''] * 9
        self.current_player: str = 'X'
        self.game_over: bool = False
        self.winner: Optional[str] = None
        self.move_count: int = 0

    def make_move(self, position: int) -> bool:
        """
        Make a move at the specified position.
        
        Args:
            position (int): The board position (0-8) where to place the move
            
        Returns:
            bool: True if the move was successful, False otherwise
            
        Raises:
            ValueError: If position is out of bounds
            IndexError: If position is already occupied
        """
        if not 0 <= position <= 8:
            raise ValueError("Position must be between 0 and 8")
        
        if self.board[position] != '':
            raise IndexError("Position already occupied")
            
        if self.game_over:
            return False
            
        self.board[position] = self.current_player
        self.move_count += 1
        
        # Check for win or draw
        if self.check_win():
            self.game_over = True
            self.winner = self.current_player
        elif self.move_count == 9:
            self.game_over = True
            self.winner = 'Draw'
            
        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        return True

    def check_win(self) -> bool:
        """
        Check if the current player has won.
        
        Returns:
            bool: True if there's a winning condition, False otherwise
        """
        # Winning combinations (rows, columns, diagonals)
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for pattern in win_patterns:
            if (self.board[pattern[0]] == self.board[pattern[1]] == 
                self.board[pattern[2]] != ''):
                return True
                
        return False

    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.move_count = 0

    def get_board_state(self) -> List[str]:
        """
        Get the current board state.
        
        Returns:
            List[str]: Current board state as list of strings
        """
        return self.board.copy()

    def get_game_status(self) -> Dict[str, Any]:
        """
        Get the current game status.
        
        Returns:
            Dict[str, Any]: Game status information
        """
        return {
            'board': self.board.copy(),
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner,
            'move_count': self.move_count
        }


class TicTacToeUI:
    """
    A class to manage the user interface components for the Tic Tac Toe game.
    
    This class provides methods to generate HTML and CSS for displaying
    the game board and handling user interactions.
    """

    def __init__(self) -> None:
        """Initialize the UI components."""
        self.game = TicTacToeGame()

    def generate_html(self) -> str:
        """
        Generate the HTML structure for the Tic Tac Toe game.
        
        Returns:
            str: Complete HTML document string
        """
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tic Tac Toe</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Tic Tac Toe</h1>
        <div id="status"></div>
        <div class="board">
            <div class="cell" data-index="0"></div>
            <div class="cell" data-index="1"></div>
            <div class="cell" data-index="2"></div>
            <div class="cell" data-index="3"></div>
            <div class="cell" data-index="4"></div>
            <div class="cell" data-index="5"></div>
            <div class="cell" data-index="6"></div>
            <div class="cell" data-index="7"></div>
            <div class="cell" data-index="8"></div>
        </div>
        <button id="reset-btn">Reset Game</button>
    </div>
    <script src="script.js"></script>
</body>
</html>
        """
        return html_content.strip()

    def generate_css(self) -> str:
        """
        Generate the CSS styling for the Tic Tac Toe game.
        
        Returns:
            str: Complete CSS style string
        """
        css_content = """
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.container {
    background-color: white;
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    text-align: center;
}

h1 {
    color: #333;
    margin-bottom: 20px;
    font-size: 2.5em;
}

#status {
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 20px;
    color: #333;
}

.board {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 20px;
    max-width: 300px;
    margin-left: auto;
    margin-right: auto;
}

.cell {
    background-color: #f0f0f0;
    border: 2px solid #333;
    border-radius: 8px;
    font-size: 2em;
    font-weight: bold;
    height: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s ease;
    min-width: 100px;
}

.cell:hover {
    background-color: #e0e0e0;
    transform: scale(1.05);
}

.cell.x {
    color: #ff4757;
}

.cell.o {
    color: #2ed573;
}

#reset-btn {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 12px 25px;
    font-size: 1.2em;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: bold;
}

#reset-btn:hover {
    background-color: #2980b9;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.winner {
    animation: pulse 1s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

@media (max-width: 480px) {
    .container {
        padding: 20px;
    }
    
    h1 {
        font-size: 2em;
    }
    
    .cell {
        height: 80px;
        font-size: 1.5em;
    }
}
        """
        return css_content.strip()

    def generate_javascript(self) -> str:
        """
        Generate the JavaScript functionality for the Tic Tac Toe game.
        
        Returns:
            str: Complete JavaScript code string
        """
        js_content = """
// Tic Tac Toe Game Implementation

class TicTacToeGame {
    constructor() {
        this.board = Array(9).fill('');
        this.currentPlayer = 'X';
        this.gameOver = false;
        this.winner = null;
        this.moveCount = 0;
    }

    makeMove(position) {
        if (position < 0 || position > 8) {
            throw new Error('Invalid position');
        }
        
        if (this.board[position] !== '') {
            throw new Error('Position already occupied');
        }
        
        if (this.gameOver) {
            return false;
        }

        this.board[position] = this.currentPlayer;
        this.moveCount++;
        
        if (this.checkWin()) {
            this.gameOver = true;
            this.winner = this.currentPlayer;
        } else if (this.moveCount === 9) {
            this.gameOver = true;
            this.winner = 'Draw';
        } else {
            this.currentPlayer = this.currentPlayer === 'X' ? 'O' : 'X';
        }
        
        return true;
    }

    checkWin() {
        const winPatterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
            [0, 4, 8], [2, 4, 6]             // Diagonals
        ];
        
        return winPatterns.some(pattern => {
            const [a, b, c] = pattern;
            return this.board[a] !== '' && 
                   this.board[a] === this.board[b] && 
                   this.board[a] === this.board[c];
        });
    }

    resetGame() {
        this.board = Array(9).fill('');
        this.currentPlayer = 'X';
        this.gameOver = false;
        this.winner = null;
        this.moveCount = 0;
    }

    getBoardState() {
        return [...this.board];
    }

    getGameStatus() {
        return {
            board: [...this.board],
            currentPlayer: this.currentPlayer,
            gameOver: this.gameOver,
            winner: this.winner,
            moveCount: this.moveCount
        };
    }
}

// DOM Elements
const cells = document.querySelectorAll('.cell');
const statusDisplay = document.getElementById('status');
const resetButton = document.getElementById('reset-btn');

// Game instance
const game = new TicTacToeGame();

// Update UI based on game state
function updateUI() {
    const status = game.getGameStatus();
    
    // Update board cells
    cells.forEach((cell, index) => {
        cell.textContent = status.board[index];
        cell.className = 'cell';
        if (status.board[index] !== '') {
            cell.classList.add(status.board[index].toLowerCase());
        }
        
        // Add animation class for winner
        if (status.winner && status.board[index] !== '') {
            cell.classList.add('winner');
        }
    });
    
    // Update status display
    if (status.gameOver) {
        if (status.winner === 'Draw') {
            statusDisplay.textContent = "It's a draw!";
        } else {
            statusDisplay.textContent = `Player ${status.winner} wins!`;
        }
    } else {
        statusDisplay.textContent = `Player ${status.currentPlayer}'s turn`;
    }
}

// Handle cell click
function handleCellClick(e) {
    const cell = e.target;
    const position = parseInt(cell.getAttribute('data-index'));
    
    try {
        game.makeMove(position);
        updateUI();
    } catch (error) {
        console.error('Error making move:', error);
    }
}

// Handle reset button click
function handleResetClick() {
    game.resetGame();
    updateUI();
}

// Event Listeners
cells.forEach(cell => {
    cell.addEventListener('click', handleCellClick);
});

resetButton.addEventListener('click', handleResetClick);

// Initialize the game
updateUI();
        """
        return js_content.strip()


def create_tic_tac_toe_game() -> Dict[str, str]:
    """
    Create a complete Tic Tac Toe game with HTML, CSS, and JavaScript.
    
    Returns:
        Dict[str, str]: Dictionary containing HTML, CSS, and JS content
    """
    ui = TicTacToeUI()
    
    return {
        'html': ui.generate_html(),
        'css': ui.generate_css(),
        'js': ui.generate_javascript()
    }


def main() -> None:
    """
    Main function to demonstrate the Tic Tac Toe game creation.
    
    This function creates a complete game package and prints its contents.
    """
    try:
        game_package = create_tic_tac_toe_game()
        
        print("=== Tic Tac Toe Game Package ===")
        print("\nHTML Content:")
        print("=" * 40)
        print(game_package['html'][:200] + "...")
        
        print("\nCSS Content:")
        print("=" * 40)
        print(game_package['css'][:200] + "...")
        
        print("\nJavaScript Content:")
        print("=" * 40)
        print(game_package['js'][:200] + "...")
        
    except Exception as e:
        print(f"Error creating Tic Tac Toe game: {e}")


if __name__ == "__main__":
    main()