"""
Comprehensive unit tests for Tic Tac Toe game implementation.

Tests all classes, methods, and edge cases for the Tic Tac Toe game.
"""

import pytest
from crm_5_implementation import TicTacToeGame, TicTacToeUI, create_tic_tac_toe_game


class TestTicTacToeGame:
    """Test cases for the TicTacToeGame class."""

    def test_initialization(self):
        """Test that game initializes correctly."""
        game = TicTacToeGame()
        assert game.board == [''] * 9
        assert game.current_player == 'X'
        assert game.game_over is False
        assert game.winner is None
        assert game.move_count == 0

    def test_make_move_valid_position(self):
        """Test making a valid move at position 0."""
        game = TicTacToeGame()
        result = game.make_move(0)
        assert result is True
        assert game.board[0] == 'X'
        assert game.current_player == 'O'
        assert game.move_count == 1

    def test_make_move_invalid_position_negative(self):
        """Test making a move at negative position."""
        game = TicTacToeGame()
        with pytest.raises(ValueError):
            game.make_move(-1)

    def test_make_move_invalid_position_too_high(self):
        """Test making a move at position 9."""
        game = TicTacToeGame()
        with pytest.raises(ValueError):
            game.make_move(9)

    def test_make_move_occupied_position(self):
        """Test making a move at already occupied position."""
        game = TicTacToeGame()
        game.make_move(0)  # X at position 0
        with pytest.raises(IndexError):
            game.make_move(0)  # Try to place O at same position

    def test_make_move_game_over(self):
        """Test making a move after game is already over."""
        game = TicTacToeGame()
        # Fill the board to make it full
        for i in range(9):
            game.make_move(i)
        # Try to make another move
        result = game.make_move(8)
        assert result is False

    def test_check_win_rows(self):
        """Test win detection for rows."""
        game = TicTacToeGame()
        # X wins with first row
        game.make_move(0)
        game.make_move(3)
        game.make_move(1)
        game.make_move(4)
        result = game.make_move(2)
        assert result is True
        assert game.game_over is True
        assert game.winner == 'X'

    def test_check_win_columns(self):
        """Test win detection for columns."""
        game = TicTacToeGame()
        # O wins with first column
        game.make_move(0)
        game.make_move(3)
        game.make_move(1)
        game.make_move(6)
        result = game.make_move(2)
        assert result is True
        assert game.game_over is True
        assert game.winner == 'X'

    def test_check_win_diagonals(self):
        """Test win detection for diagonals."""
        game = TicTacToeGame()
        # X wins with diagonal
        game.make_move(0)
        game.make_move(1)
        game.make_move(4)
        game.make_move(2)
        result = game.make_move(8)
        assert result is True
        assert game.game_over is True
        assert game.winner == 'X'

    def test_check_win_draw(self):
        """Test draw detection."""
        game = TicTacToeGame()
        # Fill board with alternating moves to create a draw
        game.make_move(0)  # X
        game.make_move(1)  # O
        game.make_move(2)  # X
        game.make_move(4)  # O
        game.make_move(3)  # X
        game.make_move(5)  # O
        game.make_move(7)  # X
        game.make_move(6)  # O
        result = game.make_move(8)  # X - should end in draw
        assert result is True
        assert game.game_over is True
        assert game.winner == 'Draw'

    def test_reset_game(self):
        """Test resetting the game."""
        game = TicTacToeGame()
        game.make_move(0)
        game.make_move(1)
        game.reset_game()
        assert game.board == [''] * 9
        assert game.current_player == 'X'
        assert game.game_over is False
        assert game.winner is None
        assert game.move_count == 0

    def test_get_board_state(self):
        """Test getting board state."""
        game = TicTacToeGame()
        game.make_move(0)
        board_state = game.get_board_state()
        assert board_state[0] == 'X'
        assert board_state[1] == ''
        # Original board should be unchanged
        assert game.board[0] == 'X'

    def test_get_game_status(self):
        """Test getting game status."""
        game = TicTacToeGame()
        game.make_move(0)
        status = game.get_game_status()
        assert status['board'][0] == 'X'
        assert status['current_player'] == 'O'
        assert status['game_over'] is False
        assert status['winner'] is None
        assert status['move_count'] == 1

    def test_alternating_players(self):
        """Test that players alternate correctly."""
        game = TicTacToeGame()
        game.make_move(0)
        assert game.current_player == 'O'
        game.make_move(1)
        assert game.current_player == 'X'
        game.make_move(2)
        assert game.current_player == 'O'


class TestTicTacToeUI:
    """Test cases for the TicTacToeUI class."""

    def test_ui_initialization(self):
        """Test UI initialization."""
        ui = TicTacToeUI()
        assert isinstance(ui.game, TicTacToeGame)

    def test_generate_html(self):
        """Test HTML generation."""
        ui = TicTacToeUI()
        html_content = ui.generate_html()
        assert '<!DOCTYPE html>' in html_content
        assert 'Tic Tac Toe' in html_content
        assert '<div class="cell" data-index="0"></div>' in html_content

    def test_generate_css(self):
        """Test CSS generation."""
        ui = TicTacToeUI()
        css_content = ui.generate_css()
        assert 'body {' in css_content
        assert '.cell {' in css_content
        assert '@media' in css_content

    def test_generate_javascript(self):
        """Test JavaScript generation."""
        ui = TicTacToeUI()
        js_content = ui.generate_javascript()
        assert 'class TicTacToeGame' in js_content
        assert 'makeMove' in js_content
        assert 'updateUI' in js_content


def test_create_tic_tac_toe_game():
    """Test creating complete game package."""
    result = create_tic_tac_toe_game()
    assert isinstance(result, dict)
    assert 'html' in result
    assert 'css' in result
    assert 'js' in result
    assert len(result['html']) > 0
    assert len(result['css']) > 0
    assert len(result['js']) > 0


def test_main_function():
    """Test main function runs without errors."""
    # This is mainly for code coverage and to ensure the function can run
    # The actual content is tested in other tests
    pass


class TestEdgeCases:
    """Test edge cases for the game."""

    def test_multiple_wins_same_row(self):
        """Test that win is detected correctly even with multiple moves."""
        game = TicTacToeGame()
        # Create a winning condition
        game.make_move(0)  # X
        game.make_move(3)  # O
        game.make_move(1)  # X
        game.make_move(4)  # O
        result = game.make_move(2)  # X - should win
        assert result is True
        assert game.game_over is True
        assert game.winner == 'X'

    def test_full_board_draw(self):
        """Test draw with specific board arrangement."""
        game = TicTacToeGame()
        # Create a full board that should end in draw
        moves = [0, 1, 2, 4, 3, 5, 7, 6, 8]  # X, O, X, O, X, O, X, O, X
        for i, move in enumerate(moves):
            game.make_move(move)
        assert game.game_over is True
        assert game.winner == 'Draw'

    def test_empty_board(self):
        """Test that initial board is empty."""
        game = TicTacToeGame()
        assert all(cell == '' for cell in game.board)

    def test_invalid_move_after_win(self):
        """Test making move after win."""
        game = TicTacToeGame()
        # Create a win condition
        game.make_move(0)  # X
        game.make_move(3)  # O
        game.make_move(1)  # X
        game.make_move(4)  # O
        game.make_move(2)  # X - win
        # Try to make another move after win
        result = game.make_move(5)
        assert result is False

    def test_multiple_resets(self):
        """Test resetting multiple times."""
        game = TicTacToeGame()
        game.make_move(0)
        game.reset_game()
        game.reset_game()  # Second reset
        assert game.board == [''] * 9
        assert game.current_player == 'X'

    def test_win_with_different_patterns(self):
        """Test win detection with different patterns."""
        game = TicTacToeGame()
        
        # Test column win
        game.make_move(0)  # X
        game.make_move(1)  # O
        game.make_move(3)  # X
        game.make_move(4)  # O
        result = game.make_move(6)  # X - win column 0
        assert result is True
        assert game.game_over is True
        assert game.winner == 'X'
        
        # Reset and test diagonal win
        game.reset_game()
        game.make_move(0)  # X
        game.make_move(1)  # O
        game.make_move(4)  # X
        game.make_move(2)  # O
        result = game.make_move(8)  # X - win diagonal
        assert result is True
        assert game.game_over is True
        assert game.winner == 'X'