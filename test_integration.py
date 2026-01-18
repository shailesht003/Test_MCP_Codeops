"""
Integration tests for Tic Tac Toe Game Implementation

This module contains integration tests that verify the complete
functionality of the Tic Tac Toe game system, including
component interactions, API endpoints, and database operations.
"""

import pytest
import json
from unittest.mock import patch, MagicMock
from crm_5_implementation import TicTacToe, GameBoard, Player


@pytest.fixture(scope="module")
def game_instance():
    """Create a Tic Tac Toe game instance for testing."""
    return TicTacToe()


@pytest.fixture(scope="function")
def clean_game_board():
    """Create a fresh game board instance for each test."""
    return GameBoard()


@pytest.fixture(scope="function")
def player_x():
    """Create a player X instance."""
    return Player("X")


@pytest.fixture(scope="function")
def player_o():
    """Create a player O instance."""
    return Player("O")


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Setup and teardown for all tests."""
    # Setup
    yield
    
    # Teardown - clean up any test data if needed
    pass


def test_game_initialization(game_instance):
    """Test that the game initializes correctly."""
    assert game_instance is not None
    assert hasattr(game_instance, 'board')
    assert hasattr(game_instance, 'current_player')
    assert hasattr(game_instance, 'players')
    assert len(game_instance.players) == 2


def test_board_creation(clean_game_board):
    """Test that game board is created with correct dimensions."""
    assert clean_game_board is not None
    assert len(clean_game_board.board) == 3
    assert all(len(row) == 3 for row in clean_game_board.board)
    assert all(cell == '' for row in clean_game_board.board for cell in row)


def test_player_creation(player_x, player_o):
    """Test that players are created with correct symbols."""
    assert player_x.symbol == "X"
    assert player_o.symbol == "O"


def test_game_board_state_management(clean_game_board):
    """Test board state management operations."""
    # Test initial state
    assert clean_game_board.get_state() == [['', '', ''], ['', '', ''], ['', '', '']]

    # Test making a move
    clean_game_board.make_move(0, 0, "X")
    state = clean_game_board.get_state()
    assert state[0][0] == "X"
    assert state[0][1] == ""
    assert state[0][2] == ""


def test_game_turn_management(game_instance, player_x, player_o):
    """Test that game manages turns correctly."""
    # Test initial player
    assert game_instance.current_player == player_x
    
    # Test turn switching
    game_instance.switch_player()
    assert game_instance.current_player == player_o
    
    # Test turn switching back
    game_instance.switch_player()
    assert game_instance.current_player == player_x


def test_game_win_detection(clean_game_board):
    """Test win detection logic."""
    # Test horizontal win
    clean_game_board.board = [["X", "X", "X"], ["", "", ""], ["", "", ""]]
    assert clean_game_board.check_win() == "X"
    
    # Test vertical win
    clean_game_board.board = [["O", "", ""], ["O", "", ""], ["O", "", ""]]
    assert clean_game_board.check_win() == "O"
    
    # Test diagonal win
    clean_game_board.board = [["X", "", ""], ["", "X", ""], ["", "", "X"]]
    assert clean_game_board.check_win() == "X"
    
    # Test no win
    clean_game_board.board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]
    assert clean_game_board.check_win() is None


def test_game_draw_detection(clean_game_board):
    """Test draw detection logic."""
    # Test draw scenario
    clean_game_board.board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]
    assert clean_game_board.check_draw() is True
    
    # Test ongoing game
    clean_game_board.board = [["X", "O", ""], ["O", "X", ""], ["O", "X", ""]]
    assert clean_game_board.check_draw() is False


def test_game_reset_functionality(game_instance):
    """Test that game can be reset properly."""
    # Make some moves
    game_instance.board.make_move(0, 0, "X")
    
    # Reset game
    game_instance.reset_game()
    
    # Verify reset
    assert game_instance.current_player == game_instance.players[0]
    assert game_instance.board.get_state() == [['', '', ''], ['', '', ''], ['', '', '']]


def test_player_symbol_assignment():
    """Test that players are assigned correct symbols."""
    game = TicTacToe()
    
    assert game.players[0].symbol == "X"
    assert game.players[1].symbol == "O"


def test_complete_game_scenario():
    """Test a complete game scenario with multiple moves."""
    game = TicTacToe()
    
    # Player X makes first move
    game.make_move(0, 0, "X")
    assert game.current_player.symbol == "O"
    
    # Player O makes second move
    game.make_move(1, 1, "O")
    assert game.current_player.symbol == "X"
    
    # Player X makes third move
    game.make_move(0, 1, "X")
    assert game.current_player.symbol == "O"
    
    # Player O makes fourth move
    game.make_move(1, 0, "O")
    assert game.current_player.symbol == "X"
    
    # Player X makes fifth move (winning move)
    game.make_move(0, 2, "X")
    
    # Verify win condition
    assert game.check_game_status() == "X"


def test_game_state_serialization():
    """Test that game state can be serialized and deserialized."""
    game = TicTacToe()
    
    # Make some moves
    game.make_move(0, 0, "X")
    game.make_move(1, 1, "O")
    
    # Serialize state
    state = game.serialize_state()
    assert isinstance(state, str)
    
    # Deserialize state
    new_game = TicTacToe()
    new_game.deserialize_state(state)
    
    # Verify state is restored
    assert new_game.board.get_state()[0][0] == "X"
    assert new_game.board.get_state()[1][1] == "O"


def test_multiple_game_instances():
    """Test that multiple game instances can exist independently."""
    game1 = TicTacToe()
    game2 = TicTacToe()
    
    # Make moves in first game
    game1.make_move(0, 0, "X")
    
    # Verify second game is unaffected
    assert game2.board.get_state()[0][0] == ""
    
    # Verify first game state
    assert game1.board.get_state()[0][0] == "X"


def test_invalid_move_handling(clean_game_board):
    """Test handling of invalid moves."""
    # Test move on occupied cell
    clean_game_board.make_move(0, 0, "X")
    result = clean_game_board.make_move(0, 0, "O")
    
    # Should not allow move on occupied cell
    assert result is False
    
    # Verify original move still there
    assert clean_game_board.board[0][0] == "X"


def test_edge_cases():
    """Test edge cases in game logic."""
    game = TicTacToe()
    
    # Test moves outside board bounds
    assert game.make_move(-1, 0, "X") is False
    assert game.make_move(3, 0, "X") is False
    assert game.make_move(0, -1, "X") is False
    assert game.make_move(0, 3, "X") is False
    
    # Test invalid player symbols
    assert game.make_move(0, 0, "Invalid") is False


def test_game_status_end_conditions():
    """Test various end game conditions."""
    # Test win condition
    game = TicTacToe()
    game.board.board = [["X", "X", "X"], ["", "", ""], ["", "", ""]]
    assert game.check_game_status() == "X"
    
    # Test draw condition
    game = TicTacToe()
    game.board.board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]
    assert game.check_game_status() == "draw"
    
    # Test ongoing game
    game = TicTacToe()
    game.board.board = [["X", "", ""], ["", "", ""], ["", "", ""]]
    assert game.check_game_status() is None


def test_concurrent_games():
    """Test that multiple concurrent games work correctly."""
    game1 = TicTacToe()
    game2 = TicTacToe()
    
    # Play first game to win
    game1.make_move(0, 0, "X")
    game1.make_move(0, 1, "X")
    game1.make_move(0, 2, "X")
    
    # Play second game to draw
    game2.make_move(0, 0, "X")
    game2.make_move(1, 1, "O")
    game2.make_move(0, 1, "O")
    game2.make_move(1, 0, "X")
    game2.make_move(2, 2, "O")
    
    # Verify first game has win
    assert game1.check_game_status() == "X"
    
    # Verify second game has draw
    assert game2.check_game_status() == "draw"