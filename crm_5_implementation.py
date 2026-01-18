"""
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
