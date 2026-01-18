import enum
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Final

class ColorTheme:
    """
    Theme Configuration Manager.
    Handles the aesthetic configuration for the Tic Tac Toe game,
    specifically implementing the CRM-8 requirement for a Green color update.
    """
    PRIMARY_COLOR: Final[str] = "Green"
    X_COLOR: Final[str] = "\033[92m"  # ANSI Green for terminal output
    O_COLOR: Final[str] = "\033[94m"  # ANSI Blue for contrast
    RESET: Final[str] = "\033[0m"
    BORDER_COLOR: Final[str] = "\033[90m"

class GameStatus(enum.Enum):
    """
    State Pattern implementation for game flow control.
    """
    IN_PROGRESS = "In Progress"
    X_WON = "X Won"
    O_WON = "O Won"
    DRAW = "Draw"

class WinStrategy(ABC):
    """
    Strategy Pattern interface for win-condition checking.
    """
    @abstractmethod
    def check_winner(self, board: List[List[Optional[str]]]) -> Optional[str]:
        """
        Determines if there is a winner on the current board.
        
        Args:
            board: 2D list representing the game board.
            
        Returns:
            Optional[str]: 'X', 'O', or None.
        """
        pass

class StandardWinStrategy(WinStrategy):
    """
    Implementation of the Strategy Pattern for standard 3x3 Tic Tac Toe rules.
    """
    def check_winner(self, board: List[List[Optional[str]]]) -> Optional[str]:
        # Check rows and columns
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0]:
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] and board[0][i]:
                return board[0][i]
        
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
            return board[0][2]
            
        return None

class GameBoardUI:
    """
    Handles the visualization of the game board.
    Incorporates the Green color theme updates.
    """
    def __init__(self, theme: ColorTheme):
        self.theme = theme

    def render(self, board: List[List[Optional[str]]], status: GameStatus, scores: Tuple[int, int]):
        """
        Renders the board to the console with the specified theme.
        """
        print(f"\n{self.theme.PRIMARY_COLOR} Tic Tac Toe - CRM-8 Update{self.theme.RESET}")
        print(f"Score: X [{scores[0]}] - O [{scores[1]}]")
        print(f"Status: {status.value}\n")
        
        for row in range(3):
            line = ""
            for col in range(3):
                cell = board[row][col]
                symbol = " "
                if cell == "X":
                    symbol = f"{self.theme.X_COLOR}X{self.theme.RESET}"
                elif cell == "O":
                    symbol = f"{self.theme.O_COLOR}O{self.theme.RESET}"
                
                line += f" {symbol} "
                if col < 2:
                    line += f"{self.theme.BORDER_COLOR}|{self.theme.RESET}"
            print(line)
            if row < 2:
                print(f"{self.theme.BORDER_COLOR}-----------{self.theme.RESET}")
        print("\n")

class GameLogicController:
    """
    Main controller coordinating the game state, logic, and UI.
    """
    def __init__(self, win_strategy: WinStrategy, theme: ColorTheme):
        self.board: List[List[Optional[str]]] = [[None for _ in range(3)] for _ in range(3)]
        self.current_player: str = "X"
        self.status: GameStatus = GameStatus.IN_PROGRESS
        self.win_strategy = win_strategy
        self.ui = GameBoardUI(theme)
        self.scores = [0, 0]  # [X_score, O_score]

    def make_move(self, row: int, col: int) -> bool:
        """
        Executes a move on the board.
        
        Args:
            row: Row index (0-2)
            col: Column index (0-2)
            
        Returns:
            bool: True if move was successful, False otherwise.
        """
        try:
            if not (0 <= row < 3 and 0 <= col < 3):
                raise ValueError("Move out of bounds")
            
            if self.board[row][col] is not None or self.status != GameStatus.IN_PROGRESS:
                return False

            self.board[row][col] = self.current_player
            self._update_game_state()
            
            if self.status == GameStatus.IN_PROGRESS:
                self.current_player = "O" if self.current_player == "X" else "X"
            
            return True
        except (ValueError, IndexError) as e:
            print(f"Error processing move: {e}")
            return False

    def _update_game_state(self):
        """
        Internal logic to transition the game state based on win conditions.
        """
        winner = self.win_strategy.check_winner(self.board)
        
        if winner == "X":
            self.status = GameStatus.X_WON
            self.scores[0] += 1
        elif winner == "O":
            self.status = GameStatus.O_WON
            self.scores[1] += 1
        elif all(all(cell is not None for cell in row) for row in self.board):
            self.status = GameStatus.DRAW

    def reset_game(self):
        """
        Resets the board for a new round while keeping scores.
        """
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.status = GameStatus.IN_PROGRESS

    def start_loop(self):
        """
        Main production entry point for the game loop.
        """
        while True:
            self.ui.render(self.board, self.status, tuple(self.scores))
            
            if self.status != GameStatus.IN_PROGRESS:
                choice = input("Game Over! Play again? (y/n): ").lower()
                if choice == 'y':
                    self.reset_game()
                    continue
                break

            try:
                move_input = input(f"Player {self.current_player}, enter move (row col) 0-2: ")
                r, c = map(int, move_input.split())
                if not self.make_move(r, c):
                    print("Invalid move, try again.")
            except ValueError:
                print("Invalid input. Please enter two numbers separated by a space.")

if __name__ == "__main__":
    # Dependency Injection for production-ready architecture
    theme_manager = ColorTheme()
    strategy = StandardWinStrategy()
    
    game = GameLogicController(strategy, theme_manager)
    game.start_loop()