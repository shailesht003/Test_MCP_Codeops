import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from crm_8_implementation import (
    ColorTheme,
    GameStatus,
    StandardWinStrategy,
    GameBoardUI,
    GameLogicController
)

@pytest.fixture
def theme():
    """Fixture for ColorTheme instance."""
    return ColorTheme()

@pytest.fixture
def win_strategy():
    """Fixture for StandardWinStrategy instance."""
    return StandardWinStrategy()

@pytest.fixture
def game_controller(win_strategy, theme):
    """Fixture for GameLogicController instance."""
    return GameLogicController(win_strategy, theme)

class TestColorTheme:
    def test_theme_constants(self, theme):
        """Verify that the theme constants are correctly defined for CRM-8."""
        assert theme.PRIMARY_COLOR == "Green"
        assert theme.X_COLOR == "\033[92m"
        assert theme.O_COLOR == "\033[94m"
        assert theme.RESET == "\033[0m"
        assert theme.BORDER_COLOR == "\033[90m"

class TestStandardWinStrategy:
    def test_empty_board(self, win_strategy):
        """Ensure no winner is detected on an empty board."""
        board = [[None for _ in range(3)] for _ in range(3)]
        assert win_strategy.check_winner(board) is None

    @pytest.mark.parametrize("row_idx", [0, 1, 2])
    def test_row_wins(self, win_strategy, row_idx):
        """Test all horizontal win conditions for both players."""
        for player in ["X", "O"]:
            board = [[None for _ in range(3)] for _ in range(3)]
            board[row_idx] = [player, player, player]
            assert win_strategy.check_winner(board) == player

    @pytest.mark.parametrize("col_idx", [0, 1, 2])
    def test_column_wins(self, win_strategy, col_idx):
        """Test all vertical win conditions for both players."""
        for player in ["X", "O"]:
            board = [[None for _ in range(3)] for _ in range(3)]
            for r in range(3):
                board[r][col_idx] = player
            assert win_strategy.check_winner(board) == player

    def test_diagonal_wins(self, win_strategy):
        """Test both diagonal win conditions."""
        # Main diagonal
        board1 = [["X", None, None], [None, "X", None], [None, None, "X"]]
        assert win_strategy.check_winner(board1) == "X"
        
        # Anti-diagonal
        board2 = [[None, None, "O"], [None, "O", None], ["O", None, None]]
        assert win_strategy.check_winner(board2) == "O"

    def test_no_winner_partial_board(self, win_strategy):
        """Test that no winner is returned when the board is partially filled but no win exists."""
        board = [
            ["X", "O", "X"],
            [None, "X", None],
            ["O", None, "O"]
        ]
        assert win_strategy.check_winner(board) is None

class TestGameBoardUI:
    def test_render_output(self, theme):
        """Verify that the render method executes without error and contains theme strings."""
        ui = GameBoardUI(theme)
        board = [["X", "O", None], [None, None, None], [None, None, None]]
        scores = (1, 0)
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            ui.render(board, GameStatus.IN_PROGRESS, scores)
            output = fake_out.getvalue()
            assert "Green Tic Tac Toe" in output
            assert "Score: X [1] - O [0]" in output
            assert "\033[92mX" in output  # Green X
            assert "\033[94mO" in output  # Blue O

class TestGameLogicController:
    def test_initialization(self, game_controller):
        """Check if the game starts with the correct initial state."""
        assert game_controller.current_player == "X"
        assert game_controller.status == GameStatus.IN_PROGRESS
        assert game_controller.scores == [0, 0]
        assert all(all(cell is None for cell in row) for row in game_controller.board)

    def test_valid_move(self, game_controller):
        """Test making a valid move updates the board and switches player."""
        success = game_controller.make_move(0, 0)
        assert success is True
        assert game_controller.board[0][0] == "X"
        assert game_controller.current_player == "O"

    def test_invalid_move_occupied(self, game_controller):
        """Test that moving to an occupied cell returns False and doesn't switch player."""
        game_controller.make_move(1, 1)
        success = game_controller.make_move(1, 1)
        assert success is False
        assert game_controller.current_player == "O"

    def test_move_out_of_bounds(self, game_controller):
        """Test that moves outside the 3x3 grid are handled gracefully."""
        with patch('sys.stdout', new=StringIO()):
            assert game_controller.make_move(3, 0) is False
            assert game_controller.make_move(-1, 2) is False

    def test_win_updates_score_and_status(self, game_controller):
        """Verify that a winning move updates the score and game status."""
        # X wins on top row
        game_controller.make_move(0, 0) # X
        game_controller.make_move(1, 0) # O
        game_controller.make_move(0, 1) # X
        game_controller.make_move(1, 1) # O
        game_controller.make_move(0, 2) # X
        
        assert game_controller.status == GameStatus.X_WON
        assert game_controller.scores == [1, 0]
        # Ensure player doesn't switch after win
        assert game_controller.current_player == "X"

    def test_draw_condition(self, game_controller):
        """Verify that a full board with no winner results in a DRAW status."""
        moves = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 0), (1, 2), (2, 1), (2, 0), (2, 2)]
        for r, c in moves:
            game_controller.make_move(r, c)
        
        assert game_controller.status == GameStatus.DRAW
        assert game_controller.scores == [0, 0]

    def test_reset_game(self, game_controller):
        """Verify that resetting the game clears the board but preserves scores."""
        game_controller.make_move(0, 0)
        game_controller.scores = [5, 3]
        game_controller.status = GameStatus.X_WON
        
        game_controller.reset_game()
        assert game_controller.status == GameStatus.IN_PROGRESS
        assert game_controller.current_player == "X"
        assert game_controller.scores == [5, 3]
        assert all(all(cell is None for cell in row) for row in game_controller.board)

    def test_move_after_game_over(self, game_controller):
        """Ensure moves are rejected if the game status is not IN_PROGRESS."""
        game_controller.status = GameStatus.X_WON
        success = game_controller.make_move(0, 0)
        assert success is False

    @patch('builtins.input')
    def test_start_loop_quit(self, mock_input, game_controller):
        """Test the game loop termination when user chooses not to play again."""
        # Setup: Win the game immediately then input 'n'
        game_controller.status = GameStatus.X_WON
        mock_input.side_effect = ['n']
        
        with patch('sys.stdout', new=StringIO()):
            game_controller.start_loop()
        
        assert mock_input.called

    @patch('builtins.input')
    def test_start_loop_play_again(self, mock_input, game_controller):
        """Test the game loop reset functionality."""
        # Setup: Win, play again ('y'), then quit ('n')
        game_controller.status = GameStatus.X_WON
        mock_input.side_effect = ['y', 'n']
        
        with patch('sys.stdout', new=StringIO()):
            # We need to mock make_move to prevent infinite loop if status doesn't change
            # But here we manually set status to X_WON to trigger the choice
            with patch.object(GameLogicController, 'reset_game', wraps=game_controller.reset_game) as mock_reset:
                game_controller.start_loop()
                assert mock_reset.called

    @patch('builtins.input')
    def test_start_loop_invalid_input(self, mock_input, game_controller):
        """Test the game loop handling of malformed input."""
        # Setup: Provide bad input, then a valid move, then win/quit
        mock_input.side_effect = ['invalid', '0 0', 'n']
        
        # Mock make_move to change status to end loop
        def side_effect_move(r, c):
            game_controller.status = GameStatus.X_WON
            return True
        
        with patch.object(game_controller, 'make_move', side_effect=side_effect_move):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                game_controller.start_loop()
                assert "Invalid input" in fake_out.getvalue()

    def test_make_move_exception_handling(self, game_controller):
        """Test that make_move catches unexpected index errors."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Trigger IndexError manually through logic if possible, or just check the try-except
            result = game_controller.make_move(10, 10)
            assert result is False
            assert "Error processing move" in fake_out.getvalue()

    def test_o_win_updates_score(self, game_controller):
        """Verify O winning increments O's score."""
        # X: (0,0), O: (1,0), X: (0,1), O: (1,1), X: (2,2), O: (1,2)
        moves = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (1, 2)]
        for r, c in moves:
            game_controller.make_move(r, c)
        
        assert game_controller.status == GameStatus.O_WON
        assert game_controller.scores == [0, 1]

if __name__ == "__main__":
    pytest.main([__file__])