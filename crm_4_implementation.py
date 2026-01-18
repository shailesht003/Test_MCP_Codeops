import tkinter as tk
from tkinter import messagebox
import math
import random
from enum import Enum
from typing import List, Tuple, Optional, Callable, Dict, Union
from abc import ABC, abstractmethod

# --- Constants & Configuration (Tailwind-inspired Palette) ---
class Theme:
    PRIMARY = "#4F46E5"      # Indigo 600
    SECONDARY = "#10B981"    # Emerald 500
    BACKGROUND = "#F8FAFC"   # Slate 50
    SURFACE = "#FFFFFF"      # White
    TEXT_MAIN = "#1E293B"    # Slate 800
    TEXT_MUTED = "#64748B"   # Slate 500
    ACCENT_X = "#EF4444"     # Red 500
    ACCENT_O = "#3B82F6"     # Blue 500
    GRID_LINE = "#E2E8F0"    # Slate 200
    FONT_FAMILY = ("Inter", "Segoe UI", "sans-serif")

class Player(Enum):
    X = "X"
    O = "O"
    EMPTY = ""

class GameStatus(Enum):
    PLAYING = "playing"
    DRAW = "draw"
    WIN_X = "win_x"
    WIN_O = "win_o"

# --- Strategy Pattern for AI ---

class AIStrategy(ABC):
    @abstractmethod
    def get_move(self, board: List[List[Player]]) -> Optional[Tuple[int, int]]:
        """Calculate the next best move for the AI."""
        pass

class MinimaxAI(AIStrategy):
    """
    Implementation of the Minimax algorithm with Alpha-Beta Pruning.
    This provides an unbeatable AI for Tic Tac Toe.
    """
    def __init__(self, ai_player: Player, opponent: Player):
        self.ai_player = ai_player
        self.opponent = opponent

    def get_move(self, board: List[List[Player]]) -> Optional[Tuple[int, int]]:
        best_score = -math.inf
        move = None
        
        for r in range(3):
            for c in range(3):
                if board[r][c] == Player.EMPTY:
                    board[r][c] = self.ai_player
                    score = self._minimax(board, 0, False, -math.inf, math.inf)
                    board[r][c] = Player.EMPTY
                    if score > best_score:
                        best_score = score
                        move = (r, c)
        return move

    def _minimax(self, board: List[List[Player]], depth: int, is_maximizing: bool, alpha: float, beta: float) -> int:
        res = self._check_winner(board)
        if res == self.ai_player: return 10 - depth
        if res == self.opponent: return depth - 10
        if self._is_board_full(board): return 0

        if is_maximizing:
            best_score = -math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == Player.EMPTY:
                        board[r][c] = self.ai_player
                        score = self._minimax(board, depth + 1, False, alpha, beta)
                        board[r][c] = Player.EMPTY
                        best_score = max(score, best_score)
                        alpha = max(alpha, score)
                        if beta <= alpha: break
            return best_score
        else:
            best_score = math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == Player.EMPTY:
                        board[r][c] = self.opponent
                        score = self._minimax(board, depth + 1, True, alpha, beta)
                        board[r][c] = Player.EMPTY
                        best_score = min(score, best_score)
                        beta = min(beta, score)
                        if beta <= alpha: break
            return best_score

    def _check_winner(self, board: List[List[Player]]) -> Optional[Player]:
        # Rows, Cols, Diagonals
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != Player.EMPTY: return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != Player.EMPTY: return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != Player.EMPTY: return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != Player.EMPTY: return board[0][2]
        return None

    def _is_board_full(self, board: List[List[Player]]) -> bool:
        return all(cell != Player.EMPTY for row in board for cell in row)

# --- Model: Game Engine ---

class GameEngine:
    """Core logic and state management for Tic Tac Toe."""
    def __init__(self):
        self.board: List[List[Player]] = [[Player.EMPTY for _ in range(3)] for _ in range(3)]
        self.current_turn: Player = Player.X
        self.status: GameStatus = GameStatus.PLAYING
        self.observers: List[Callable] = []

    def add_observer(self, callback: Callable):
        """Observer pattern to notify UI of state changes."""
        self.observers.append(callback)

    def _notify(self):
        for callback in self.observers:
            callback()

    def make_move(self, row: int, col: int) -> bool:
        """Process a player move."""
        if self.status != GameStatus.PLAYING or self.board[row][col] != Player.EMPTY:
            return False

        self.board[row][col] = self.current_turn
        self._update_status()
        
        if self.status == GameStatus.PLAYING:
            self.current_turn = Player.O if self.current_turn == Player.X else Player.X
            
        self._notify()
        return True

    def _update_status(self):
        winner = self._get_winner()
        if winner == Player.X:
            self.status = GameStatus.WIN_X
        elif winner == Player.O:
            self.status = GameStatus.WIN_O
        elif all(cell != Player.EMPTY for row in self.board for cell in row):
            self.status = GameStatus.DRAW
        else:
            self.status = GameStatus.PLAYING

    def _get_winner(self) -> Optional[Player]:
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != Player.EMPTY: return self.board[i][0]
            if self.board[0][i] == board[1][i] == board[2][i] != Player.EMPTY: return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != Player.EMPTY: return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != Player.EMPTY: return self.board[0][2]
        return None

    def reset(self):
        """Reset the game state."""
        self.board = [[Player.EMPTY for _ in range(3)] for _ in range(3)]
        self.current_turn = Player.X
        self.status = GameStatus.PLAYING
        self._notify()

# --- Asset & Animation Controller ---

class AnimationController:
    """Simulates smooth UI transitions using Tkinter's event loop."""
    @staticmethod
    def fade_in(widget: tk.Widget, duration: int = 200):
        def effect(alpha: float):
            if alpha <= 1.0:
                # Note: Windows/Linux specific transparency logic usually requires 
                # specialized libraries, so we simulate with color stepping or visibility
                pass
        # Simulation of animation delay
        widget.after(duration, lambda: widget.config(state="normal"))

# --- View: Fancy UI Layer ---

class TicTacToeUI(tk.Tk):
    """The main UI Rendering Layer using Tkinter."""
    def __init__(self, engine: GameEngine, ai: Optional[AIStrategy] = None):
        super().__init__()
        self.engine = engine
        self.ai = ai
        self.buttons: List[List[tk.Button]] = []
        
        self.title("Tic Tac Toe - Premium Edition")
        self.geometry("450x600")
        self.configure(bg=Theme.BACKGROUND)
        self.resizable(False, False)
        
        self._setup_layout()
        self.engine.add_observer(self.render)

    def _setup_layout(self):
        """Initialize the UI components."""
        # Header
        self.header_frame = tk.Frame(self, bg=Theme.BACKGROUND, pady=30)
        self.header_frame.pack(fill="x")
        
        self.status_label = tk.Label(
            self.header_frame, 
            text="Player X's Turn", 
            font=(Theme.FONT_FAMILY[0], 24, "bold"),
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT_MAIN
        )
        self.status_label.pack()

        # Grid Container
        self.grid_container = tk.Frame(self, bg=Theme.GRID_LINE, padx=2, pady=2)
        self.grid_container.pack(padx=40, pady=20)

        for r in range(3):
            row_buttons = []
            for c in range(3):
                btn = tk.Button(
                    self.grid_container,
                    text="",
                    font=(Theme.FONT_FAMILY[0], 32, "bold"),
                    width=4,
                    height=2,
                    relief="flat",
                    bg=Theme.SURFACE,
                    activebackground=Theme.BACKGROUND,
                    command=lambda r=r, c=c: self._handle_click(r, c)
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Footer / Controls
        self.footer_frame = tk.Frame(self, bg=Theme.BACKGROUND, pady=30)
        self.footer_frame.pack(fill="x")
        
        self.reset_btn = tk.Button(
            self.footer_frame,
            text="Reset Game",
            font=(Theme.FONT_FAMILY[0], 12, "bold"),
            bg=Theme.PRIMARY,
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
            cursor="hand2",
            command=self.engine.reset
        )
        self.reset_btn.pack()

    def _handle_click(self, r: int, c: int):
        """User interaction handler."""
        if self.engine.current_turn == Player.X or self.ai is None:
            if self.engine.make_move(r, c):
                if self.ai and self.engine.status == GameStatus.PLAYING:
                    # Trigger AI move after a short delay for 'animation' feel
                    self.after(600, self._trigger_ai)

    def _trigger_ai(self):
        """Execute AI logic and update UI."""
        move = self.ai.get_move(self.engine.board)
        if move:
            self.engine.make_move(move[0], move[1])

    def render(self):
        """Update the UI based on the current engine state."""
        # Update Board
        for r in range(3):
            for c in range(3):
                val = self.engine.board[r][c].value
                color = Theme.ACCENT_X if val == "X" else Theme.ACCENT_O
                self.buttons[r][c].config(
                    text=val,
                    fg=color,
                    state="disabled" if val != "" else "normal"
                )

        # Update Status Label
        if self.engine.status == GameStatus.PLAYING:
            self.status_label.config(
                text=f"Player {self.engine.current_turn.value}'s Turn",
                fg=Theme.TEXT_MAIN
            )
        elif self.engine.status == GameStatus.DRAW:
            self.status_label.config(text="It's a Draw!", fg=Theme.TEXT_MUTED)
            self._disable_all()
        else:
            winner = "X" if self.engine.status == GameStatus.WIN_X else "O"
            self.status_label.config(text=f"Player {winner} Wins!", fg=Theme.SECONDARY)
            self._disable_all()

    def _disable_all(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

# --- Main Application Controller ---

class TicTacToeApp:
    """Main entry point for the application."""
    def __init__(self):
        try:
            # Initialize Engine
            self.engine = GameEngine()
            
            # Setup AI (Minimax) - Computer plays as 'O'
            self.ai_strategy = MinimaxAI(ai_player=Player.O, opponent=Player.X)
            
            # Initialize View
            self.ui = TicTacToeUI(self.engine, ai=self.ai_strategy)
            
        except Exception as e:
            self._handle_critical_error(e)

    def _handle_critical_error(self, e: Exception):
        """Basic error handling for production stability."""
        print(f"Critical Error: {e}")
        # In a real production app, log to a file or monitoring service

    def run(self):
        """Start the main event loop."""
        self.ui.mainloop()

if __name__ == "__main__":
    # Ensure the app runs as a standalone script
    app = TicTacToeApp()
    app.run()