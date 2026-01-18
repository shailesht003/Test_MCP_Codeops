"""
Integration tests for Tic Tac Toe Game Implementation

These tests verify the integration between HTML, CSS, JavaScript components
and the Python backend implementation.
"""

import pytest
from unittest.mock import Mock, patch
from crm_5_implementation import Player, GameStatus, TicTacToeGame


@pytest.fixture
def game_instance():
    """Fixture to create a Tic Tac Toe game instance."""
    return TicTacToeGame()


@pytest.fixture
def mock_db_connection():
    """Fixture to mock database connection."""
    with patch('crm_5_implementation.create_db_connection') as mock_conn:
        mock_db = Mock()
        mock_conn.return_value = mock_db
        yield mock_db


def test_game_initialization(game_instance):
    """Test that the game initializes correctly."""
    assert game_instance.board == [["", "", ""], ["", "", ""], ["", "", ""]]
    assert game_instance.current_player == Player.X
    assert game_instance.status == GameStatus.PLAYING


def test_game_move_validation(game_instance):
    """Test valid and invalid moves."""
    # Valid move
    result = game_instance.make_move(0, 0)
    assert result is True
    assert game_instance.board[0][0] == "X"
    
    # Invalid move - position already taken
    result = game_instance.make_move(0, 0)
    assert result is False
    
    # Invalid move - out of bounds
    result = game_instance.make_move(5, 5)
    assert result is False


def test_game_win_detection(game_instance):
    """Test win detection for different scenarios."""
    # Test horizontal win
    game_instance.make_move(0, 0)  # X
    game_instance.make_move(1, 0)  # O
    game_instance.make_move(0, 1)  # X
    game_instance.make_move(1, 1)  # O
    game_instance.make_move(0, 2)  # X
    
    assert game_instance.status == GameStatus.X_WON


def test_game_draw_detection(game_instance):
    """Test draw detection when board is full with no winner."""
    moves = [
        (0, 0), (1, 1), (0, 1), (1, 0), (0, 2),
        (2, 0), (2, 1), (2, 2), (1, 2)
    ]
    
    for i, (row, col) in enumerate(moves):
        game_instance.make_move(row, col)
    
    assert game_instance.status == GameStatus.DRAW


def test_game_reset(game_instance):
    """Test game reset functionality."""
    game_instance.make_move(0, 0)
    game_instance.reset_game()
    
    assert game_instance.board == [["", "", ""], ["", "", ""], ["", "", ""]]
    assert game_instance.current_player == Player.X
    assert game_instance.status == GameStatus.PLAYING


def test_game_state_serialization(game_instance):
    """Test serialization of game state."""
    game_instance.make_move(0, 0)
    
    state = game_instance.serialize_state()
    assert "board" in state
    assert "current_player" in state
    assert "status" in state


def test_game_database_integration(game_instance, mock_db_connection):
    """Test integration with database operations."""
    # Mock successful save
    mock_db_connection.execute.return_value = None
    
    game_instance.make_move(0, 0)
    game_instance.save_to_database()
    
    mock_db_connection.execute.assert_called_once()


def test_game_database_load_integration(game_instance, mock_db_connection):
    """Test database load functionality."""
    # Mock database data
    mock_data = {
        "board": [["X", "", ""], ["", "", ""], ["", "", ""]],
        "current_player": "O",
        "status": "playing"
    }
    
    mock_db_connection.fetchone.return_value = json.dumps(mock_data)
    
    game_instance.load_from_database()
    
    assert game_instance.board[0][0] == "X"
    assert game_instance.current_player == Player.O


def test_game_html_output_generation(game_instance):
    """Test HTML output generation for game display."""
    html_output = game_instance.generate_html_output()
    
    assert "<table" in html_output
    assert "Tic Tac Toe" in html_output
    assert "X" in html_output or "O" in html_output


def test_game_css_output_generation(game_instance):
    """Test CSS output generation for styling."""
    css_output = game_instance.generate_css_output()
    
    assert "background-color" in css_output
    assert "border" in css_output
    assert "font-size" in css_output


def test_game_javascript_output_generation(game_instance):
    """Test JavaScript output generation for interactivity."""
    js_output = game_instance.generate_js_output()
    
    assert "onclick" in js_output
    assert "game" in js_output
    assert "function" in js_output


def test_game_full_integration_scenario(game_instance):
    """Test complete integration scenario with multiple operations."""
    # Start game and make moves
    assert game_instance.status == GameStatus.PLAYING
    
    # Make several moves
    game_instance.make_move(0, 0)  # X
    game_instance.make_move(1, 1)  # O
    
    assert game_instance.current_player == Player.X
    assert game_instance.board[0][0] == "X"
    
    # Check state serialization
    serialized = game_instance.serialize_state()
    assert isinstance(serialized, dict)
    
    # Test HTML generation
    html = game_instance.generate_html_output()
    assert "<table" in html
    
    # Test CSS generation
    css = game_instance.generate_css_output()
    assert "background-color" in css
    
    # Test reset
    game_instance.reset_game()
    assert game_instance.status == GameStatus.PLAYING


def test_game_edge_cases(game_instance):
    """Test edge cases and boundary conditions."""
    # Test empty board
    assert game_instance.board[0][0] == ""
    
    # Test invalid coordinates
    assert game_instance.make_move(-1, -1) is False
    assert game_instance.make_move(3, 3) is False
    
    # Test alternating players
    game_instance.make_move(0, 0)
    assert game_instance.current_player == Player.O
    
    game_instance.make_move(1, 1)
    assert game_instance.current_player == Player.X


def test_game_multiple_scenarios(game_instance):
    """Test multiple game scenarios."""
    # Scenario 1: X wins vertically
    game_instance.make_move(0, 0)  # X
    game_instance.make_move(0, 1)  # O
    game_instance.make_move(1, 0)  # X
    game_instance.make_move(1, 1)  # O
    game_instance.make_move(2, 0)  # X
    
    assert game_instance.status == GameStatus.X_WON
    
    # Reset and test O win
    game_instance.reset_game()
    
    game_instance.make_move(0, 0)  # X
    game_instance.make_move(0, 1)  # O
    game_instance.make_move(1, 0)  # X
    game_instance.make_move(1, 1)  # O
    game_instance.make_move(2, 1)  # X
    game_instance.make_move(2, 2)  # O
    
    assert game_instance.status == GameStatus.O_WON


def test_game_concurrent_moves(game_instance):
    """Test handling of concurrent moves in sequence."""
    # Simulate multiple players making moves
    moves = [(0, 0), (1, 1), (0, 1), (1, 0), (0, 2)]
    
    for i, (row, col) in enumerate(moves):
        result = game_instance.make_move(row, col)
        assert result is True
    
    # Verify all moves were made
    assert game_instance.board[0][0] == "X"
    assert game_instance.board[1][1] == "O"
    assert game_instance.board[0][1] == "X"
    assert game_instance.board[1][0] == "O"
    assert game_instance.board[0][2] == "X"


def test_game_setup_teardown(game_instance):
    """Test proper setup and teardown of game components."""
    # Initial state check
    assert game_instance.current_player == Player.X
    assert game_instance.status == GameStatus.PLAYING
    
    # Make some moves
    game_instance.make_move(0, 0)
    
    # Verify state change
    assert game_instance.board[0][0] == "X"
    
    # Reset and verify clean state
    game_instance.reset_game()
    assert game_instance.current_player == Player.X
    assert game_instance.status == GameStatus.PLAYING
    assert all(all(cell == "" for cell in row) for row in game_instance.board)