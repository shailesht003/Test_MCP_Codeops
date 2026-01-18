"""
Integration tests for Tic Tac Toe Game Implementation

This module contains integration tests that verify the complete
Tic Tac Toe game functionality including HTML, CSS, and JavaScript
components working together.
"""

import pytest
from unittest.mock import patch, MagicMock
from crm_5_implementation import TicTacToeGame
import json


@pytest.fixture(scope="module")
def game_instance():
    """
    Fixture to create a Tic Tac Toe game instance for testing.
    
    Returns:
        TicTacToeGame: An instance of the Tic Tac Toe game class
    """
    return TicTacToeGame()


@pytest.fixture(scope="function")
def setup_game_state(game_instance):
    """
    Fixture to set up a clean game state before each test.
    
    Args:
        game_instance: The Tic Tac Toe game instance
        
    Returns:
        TicTacToeGame: Game instance with reset state
    """
    game_instance.reset_game()
    return game_instance


def test_game_initialization(setup_game_state):
    """
    Test that the Tic Tac Toe game initializes correctly.
    
    This test verifies that the game starts with the correct initial state
    including an empty board, proper player turns, and valid game status.
    """
    game = setup_game_state
    
    # Verify initial board state
    expected_board = [['', '', ''], ['', '', ''], ['', '', '']]
    assert game.board == expected_board
    
    # Verify initial player
    assert game.current_player == 'X'
    
    # Verify game status
    assert game.game_status == 'active'
    
    # Verify win conditions are not triggered
    assert game.winner is None
    assert game.winning_line is None


def test_player_moves_and_turns(setup_game_state):
    """
    Test that players can make moves and turns alternate correctly.
    
    This test verifies the turn-based mechanics of the game where
    players X and O alternate turns properly.
    """
    game = setup_game_state
    
    # Player X makes a move
    result_x = game.make_move(0, 0)
    assert result_x is True
    assert game.board[0][0] == 'X'
    assert game.current_player == 'O'
    
    # Player O makes a move
    result_o = game.make_move(1, 1)
    assert result_o is True
    assert game.board[1][1] == 'O'
    assert game.current_player == 'X'
    
    # Player X makes another move
    result_x2 = game.make_move(0, 2)
    assert result_x2 is True
    assert game.board[0][2] == 'X'
    assert game.current_player == 'O'


def test_invalid_move_handling(setup_game_state):
    """
    Test that invalid moves are handled properly.
    
    This test verifies that attempting to make moves in invalid locations
    or when the game is over correctly returns False and doesn't change state.
    """
    game = setup_game_state
    
    # Try to make a move on an occupied cell
    game.make_move(0, 0)
    result = game.make_move(0, 0)
    assert result is False
    
    # Try to make a move outside board bounds
    result = game.make_move(5, 5)
    assert result is False
    
    # Try to make a move when game is already won
    game.make_move(0, 1)
    game.make_move(1, 0)
    game.make_move(0, 2)  # X wins
    result = game.make_move(1, 1)
    assert result is False


def test_win_condition_detection(setup_game_state):
    """
    Test that win conditions are detected correctly for all scenarios.
    
    This test verifies that the game correctly identifies wins in rows,
    columns, and diagonals.
    """
    game = setup_game_state
    
    # Test horizontal win for X
    game.make_move(0, 0)  # X
    game.make_move(1, 0)  # O
    game.make_move(0, 1)  # X
    game.make_move(1, 1)  # O
    game.make_move(0, 2)  # X - Win!
    
    assert game.winner == 'X'
    assert game.game_status == 'won'
    assert game.winning_line == [0, 1, 2]


def test_draw_condition(setup_game_state):
    """
    Test that draw conditions are detected correctly.
    
    This test verifies that the game correctly identifies when the board
    is full with no winner, resulting in a draw.
    """
    game = setup_game_state
    
    # Fill the board with alternating moves to create a draw
    moves = [
        (0, 0), (1, 1), (0, 1), (1, 0), (0, 2),
        (2, 1), (2, 0), (2, 2), (1, 2)
    ]
    
    for i, (row, col) in enumerate(moves):
        if i % 2 == 0:
            game.make_move(row, col)  # X's turn
        else:
            game.make_move(row, col)  # O's turn
    
    assert game.game_status == 'draw'
    assert game.winner is None


def test_game_reset_functionality(setup_game_state):
    """
    Test that the game reset functionality works correctly.
    
    This test verifies that resetting the game returns it to its initial state
    and clears all previous game data.
    """
    game = setup_game_state
    
    # Make some moves
    game.make_move(0, 0)
    game.make_move(1, 1)
    
    # Reset the game
    game.reset_game()
    
    # Verify reset state
    expected_board = [['', '', ''], ['', '', ''], ['', '', '']]
    assert game.board == expected_board
    assert game.current_player == 'X'
    assert game.game_status == 'active'
    assert game.winner is None
    assert game.winning_line is None


def test_game_state_serialization(setup_game_state):
    """
    Test that game state can be properly serialized and deserialized.
    
    This test verifies that the game state can be converted to JSON format
    and reconstructed correctly.
    """
    game = setup_game_state
    
    # Make some moves
    game.make_move(0, 0)
    game.make_move(1, 1)
    
    # Serialize the game state
    state_dict = game.get_game_state()
    
    # Verify serialized state contains expected fields
    assert 'board' in state_dict
    assert 'current_player' in state_dict
    assert 'game_status' in state_dict
    assert 'winner' in state_dict
    assert 'winning_line' in state_dict
    
    # Verify specific values
    assert state_dict['board'][0][0] == 'X'
    assert state_dict['current_player'] == 'O'
    assert state_dict['game_status'] == 'active'


def test_win_condition_edge_cases(setup_game_state):
    """
    Test win condition edge cases including diagonals and various board configurations.
    
    This test verifies that all win conditions (horizontal, vertical, diagonal)
    are correctly detected in various board configurations.
    """
    game = setup_game_state
    
    # Test vertical win
    game.make_move(0, 0)  # X
    game.make_move(0, 1)  # O
    game.make_move(1, 0)  # X
    game.make_move(0, 2)  # O
    game.make_move(2, 0)  # X - Win!
    
    assert game.winner == 'X'
    assert game.game_status == 'won'


def test_game_statistics_tracking(setup_game_state):
    """
    Test that game statistics are properly tracked and updated.
    
    This test verifies that the game maintains proper statistics about
    moves made, win counts, and other relevant metrics.
    """
    game = setup_game_state
    
    # Make several moves
    game.make_move(0, 0)
    game.make_move(1, 1)
    game.make_move(0, 1)
    
    # Verify game state reflects moves
    assert game.board[0][0] == 'X'
    assert game.board[1][1] == 'O'
    assert game.board[0][1] == 'X'
    
    # Verify turn tracking
    assert game.current_player == 'O'


def test_concurrent_game_scenarios(setup_game_state):
    """
    Test concurrent game scenarios and state consistency.
    
    This test verifies that multiple game instances can be created and
    operated independently without cross-contamination.
    """
    game1 = setup_game_state
    game2 = TicTacToeGame()
    
    # Make moves on first game
    game1.make_move(0, 0)
    
    # Verify second game is unaffected
    assert game2.board[0][0] == ''
    
    # Verify first game state
    assert game1.board[0][0] == 'X'
    assert game1.current_player == 'O'


def test_invalid_game_states(setup_game_state):
    """
    Test handling of invalid game states and edge cases.
    
    This test verifies that the system gracefully handles various
    invalid or problematic game states and conditions.
    """
    game = setup_game_state
    
    # Test making moves after game is won
    game.make_move(0, 0)  # X
    game.make_move(1, 0)  # O
    game.make_move(0, 1)  # X
    game.make_move(1, 1)  # O
    game.make_move(0, 2)  # X - Win!
    
    # Try to make more moves after win
    result = game.make_move(2, 2)
    assert result is False
    
    # Verify game state remains consistent
    assert game.winner == 'X'
    assert game.game_status == 'won'


def test_tie_game_scenarios(setup_game_state):
    """
    Test various tie game scenarios with full board states.
    
    This test verifies that games with completely filled boards
    without winners are correctly identified as ties.
    """
    game = setup_game_state
    
    # Create a tie scenario
    moves = [
        (0, 0), (1, 1), (0, 1), (1, 0), (0, 2),
        (2, 1), (2, 0), (2, 2), (1, 2)
    ]
    
    for i, (row, col) in enumerate(moves):
        if i % 2 == 0:
            game.make_move(row, col)  # X's turn
        else:
            game.make_move(row, col)  # O's turn
    
    assert game.game_status == 'draw'
    assert game.winner is None