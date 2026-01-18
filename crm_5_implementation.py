import logging
from flask import Flask, render_template_string
from typing import Final

# Configure logging for production readiness
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TicTacToeApp:
    """
    A production-ready Flask application serving a Tic Tac Toe game.
    
    This class encapsulates the web server logic and the frontend assets 
    (HTML, CSS, JS) required to run a client-side Tic Tac Toe game 
    following the specific architectural requirements provided.
    """

    # HTML/CSS/JS Content Template
    # Following Architecture Design: HTML5, CSS3 (Grid/Flexbox), JS (ES6+ Module Pattern, Event Delegation)
    TEMPLATE: Final[str] = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CRM-5: Tic Tac Toe</title>
        <style>
            :root {
                --bg-color: #f4f7f6;
                --text-color: #333;
                --cell-size: 100px;
                --grid-gap: 10px;
                --x-color: #e74c3c;
                --o-color: #3498db;
                --winner-bg: #2ecc71;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--bg-color);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }

            .game-container {
                text-align: center;
            }

            .status-indicator {
                margin-bottom: 20px;
                font-size: 1.5rem;
                font-weight: bold;
                color: var(--text-color);
            }

            /* CSS Grid for the 3x3 Board */
            .game-board {
                display: grid;
                grid-template-columns: repeat(3, var(--cell-size));
                grid-template-rows: repeat(3, var(--cell-size));
                gap: var(--grid-gap);
                background-color: #ccc;
                padding: var(--grid-gap);
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }

            .cell {
                background-color: #fff;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2.5rem;
                font-weight: bold;
                cursor: pointer;
                transition: background-color 0.3s ease, transform 0.1s ease;
                user-select: none;
            }

            .cell:hover {
                background-color: #f9f9f9;
            }

            .cell.x { color: var(--x-color); }
            .cell.o { color: var(--o-color); }

            .cell.winner {
                background-color: var(--winner-bg);
                color: white;
            }

            .controls {
                margin-top: 30px;
            }

            button {
                padding: 10px 25px;
                font-size: 1rem;
                cursor: pointer;
                background-color: #34495e;
                color: white;
                border: none;
                border-radius: 4px;
                transition: background-color 0.2s;
            }

            button:hover {
                background-color: #2c3e50;
            }
        </style>
    </head>
    <body>

        <div class="game-container">
            <h1>Tic Tac Toe</h1>
            <div id="status" class="status-indicator">Player X's Turn</div>
            
            <div id="board" class="game-board">
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

            <div class="controls">
                <button id="reset-btn">Restart Game</button>
            </div>
        </div>

        <script>
            /**
             * Game Engine Module
             * Encapsulates game logic using the Module Pattern.
             */
            const TicTacToe = (() => {
                // State Management
                let boardState = ["", "", "", "", "", "", "", "", ""];
                let currentPlayer = "X";
                let gameActive = true;

                const winningConditions = [
                    [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
                    [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
                    [0, 4, 8], [2, 4, 6]             // Diagonals
                ];

                const statusDisplay = document.querySelector('#status');
                const cells = document.querySelectorAll('.cell');

                const handleResultValidation = () => {
                    let roundWon = false;
                    let winningLine = [];

                    for (let i = 0; i < winningConditions.length; i++) {
                        const [a, b, c] = winningConditions[i];
                        if (boardState[a] && boardState[a] === boardState[b] && boardState[a] === boardState[c]) {
                            roundWon = true;
                            winningLine = [a, b, c];
                            break;
                        }
                    }

                    if (roundWon) {
                        statusDisplay.innerText = `Player ${currentPlayer} Wins!`;
                        gameActive = false;
                        winningLine.forEach(index => cells[index].classList.add('winner'));
                        return;
                    }

                    if (!boardState.includes("")) {
                        statusDisplay.innerText = "Draw!";
                        gameActive = false;
                        return;
                    }

                    currentPlayer = currentPlayer === "X" ? "O" : "X";
                    statusDisplay.innerText = `Player ${currentPlayer}'s Turn`;
                };

                const handleCellClick = (clickedCellEvent) => {
                    // Event Delegation logic: ensure target is a cell
                    const clickedCell = clickedCellEvent.target;
                    if (!clickedCell.classList.contains('cell')) return;

                    const clickedCellIndex = parseInt(clickedCell.getAttribute('data-index'));

                    if (boardState[clickedCellIndex] !== "" || !gameActive) {
                        return;
                    }

                    boardState[clickedCellIndex] = currentPlayer;
                    clickedCell.innerText = currentPlayer;
                    clickedCell.classList.add(currentPlayer.toLowerCase());

                    handleResultValidation();
                };

                const restartGame = () => {
                    gameActive = true;
                    currentPlayer = "X";
                    boardState = ["", "", "", "", "", "", "", "", ""];
                    statusDisplay.innerText = "Player X's Turn";
                    cells.forEach(cell => {
                        cell.innerText = "";
                        cell.classList.remove('x', 'o', 'winner');
                    });
                };

                return {
                    handleCellClick,
                    restartGame
                };
            })();

            // Initialize Event Listeners using Event Delegation on the board
            document.querySelector('#board').addEventListener('click', TicTacToe.handleCellClick);
            document.querySelector('#reset-btn').addEventListener('click', TicTacToe.restartGame);
        </script>
    </body>
    </html>
    """

    def __init__(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """
        Initializes the TicTacToe Server.

        :param host: Network interface to bind to.
        :param port: Port to listen on.
        :param debug: Enable/Disable Flask debug mode.
        """
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.debug = debug
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Configures the Flask application routes."""
        @self.app.route('/')
        def index() -> str:
            """Serves the main game page."""
            try:
                return render_template_string(self.TEMPLATE)
            except Exception as e:
                logger.error(f"Error rendering template: {e}")
                return "Internal Server Error", 500

    def run(self) -> None:
        """Starts the Flask production server."""
        try:
            logger.info(f"Starting Tic Tac Toe server on {self.host}:{self.port}")
            self.app.run(host=self.host, port=self.port, debug=self.debug)
        except Exception as e:
            logger.critical(f"Failed to start server: {e}")

if __name__ == "__main__":
    # Production configuration
    game_server = TicTacToeApp(
        host='127.0.0.1', 
        port=8080, 
        debug=False
    )
    game_server.run()