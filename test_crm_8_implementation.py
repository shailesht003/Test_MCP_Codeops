import pytest
from crm_8_implementation import ConfigManager, Game

def test_config_manager_singleton():
    """Test that ConfigManager is a singleton."""
    config1 = ConfigManager()
    config2 = ConfigManager()
    assert config1 is config2, "ConfigManager should be a singleton"

def test_config_manager_default_theme():
    """Test that ConfigManager initializes with the correct default theme."""
    config = ConfigManager()
    expected_theme = {
        'board_bg': '#e0e0e0',
        'cell_border': '#b0b0b0',
        'x_color': '#555555',
        'o_color': '#555555',
        'text_color': '#333333'
    }
    assert config.get_theme() == expected_theme, "Theme configuration is incorrect"

def test_game_initial_state():
    """Test that Game initializes with an empty board and correct state."""
    game = Game()
    assert game.board == [['' for _ in range(3)] for _ in range(3)], "Board should be empty"
    assert game.current_player == 'X', "Current player should be X"
    assert game.winner is None, "Winner should be None"
    assert game.game_over is False, "Game should not be over"
    assert game.config == ConfigManager().get_theme(), "Theme should match ConfigManager"

def test_game_make_valid_move():
    """Test that a valid move updates the board and switches players."""
    game = Game()
    game.make_move(0, 0)
    assert game.board[0][0] == 'X', "Move should update the board"
    assert game.current_player == 'O', "Player should switch after valid move"
    assert game.game_over is False, "Game should not be over after valid move"

def test_game_make_invalid_move_out_of_bounds():
    """Test that making a move with out-of-bounds coordinates raises ValueError."""
    game = Game()
    with pytest.raises(ValueError, match="Row and column must be between 0 and 2"):
        game.make_move(3, 0)

def test_game_make_invalid_move_occupied_cell():
    """Test that making a move on an occupied cell raises ValueError."""
    game = Game()
    game.make_move(0, 0)
    with pytest.raises(ValueError, match="Cell already occupied"):
        game.make_move(0, 0)

def test_game_win_row():
    """Test that a win by completing a row sets the winner and ends the game."""
    game = Game()
    game.make_move(0, 0)
    game.make_move(0, 1)
    game.make_move(0, 2)
    assert game.winner == 'X', "Winner should be X after row win"
    assert game.game_over is True, "Game should be over after win"

def test_game_win_column():
    """Test that a win by completing a column sets the winner and ends the game."""
    game = Game()
    game.make_move(0, 0)
    game.make_move(1, 0)
    game.make_move(2, 0)
    assert game.winner == 'X', "Winner should be X after column win"
    assert game.game_over is True, "Game should be over after win"

def test_game_win_diagonal_top_left_to_bottom_right():
    """Test that a win by completing the main diagonal sets the winner and ends the game."""
    game = Game()
    game.make_move(0, 0)
    game.make_move(1, 1)
    game.make_move(2, 2)
    assert game.winner == 'X', "Winner should be X after diagonal win"
    assert game.game_over is True, "Game should be over after win"

def test_game_win_diagonal_top_right_to_bottom_left():
    """Test that a win by completing the anti-diagonal sets the winner and ends the game."""
    game = Game()
    game.make_move(0, 2)
    game.make_move(1, 1)
    game.make_move(2, 0)
    assert game.winner == 'X', "Winner should be X after anti-diagonal win"
    assert game.game, "Game should be over after win"

def test_game_draw():
    """Test that a full board with no winner results in a draw."""
    game = Game()
    # Fill the board with X and O alternately
    moves = [(0,0), (0,1), (0,2),
             (1,0), (1,1), (1,2),
             (2,0), (2,1), (2,2)]
    for row, col in moves:
        game.make_move(row, col)
    assert game.winner is None, "Winner should be None after draw"
    assert game.game_over is True, "Game should be over after draw"

def test_game_make_move_after_game_over():
    """Test that making a move after the game is over raises ValueError."""
    game = Game()
    game.make_move(0, 0)
    game.make_move(0, 1)
    game.make_move(0, 2)
    with pytest.raises(ValueError, match="Game is already over"):
        game.make_move(0, 0)

def test_game_reset_game():
    """Test that reset_game restores the game to its initial state."""
    game = Game()
    game.make_move(0, 0)
    game.reset_game()
    assert game.board == [['' for _ in range(3)] for _ in range(3)], "Board should be reset"
    assert game.current_player == 'X', "Current player should be X"
    assert game.winner is None, "Winner should be None"
    assert game.game_over is False, "Game should not be over"

def test_game_get_status():
    """Test that get_status returns the correct game state dictionary."""
    game = Game()
    expected_status = {
        'winner': None,
        'game_over': False,
        'current_player': 'X',
        'board': [['' for _ in range(3)] for _ in range(3)],
        'theme': ConfigManager().get_theme()
    }
    assert game.get_status() == expected_status, "Status should match expected values"

def test_game_get_board_copy():
    """Test that get_board returns a copy of the board, not the original."""
    game = Game()
    board_copy = game.get_board()
    board_copy[0][0] = 'X'
    assert game.board[0][0] == '', "Board should remain unchanged after copy modification"
    assert board_copy[0][0] == 'X', "Copy should have the modified value"

def test_game_multiple_moves_and_status():
    """Test that multiple moves update the game status correctly."""
    game = Game()
    game.make_move(0, 0)
    game.make_move(1, 1)
    game.make_move(2, 2)
    status = game.get_status()
    assert status['winner'] == 'X', "Winner should be X after diagonal win"
    assert status['game_over'] is True, "Game should be over after win"
    assert status['board'][0][0] == 'X', "Board should reflect the moves"
    assert status['current_player'] == 'O', "Current player should be O after X's move"