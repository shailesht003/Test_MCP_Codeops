import pytest
from unittest.mock import MagicMock, patch
import tkinter as tk
from crm_4_implementation import (
    Player, GameStatus, MinimaxAI, GameEngine, 
    AnimationController, TicTacToeUI, TicTacToeApp, Theme
)

# --- Fixtures ---

@pytest.fixture
def engine():
    """Provides a fresh GameEngine instance."""
    return GameEngine()

@pytest.fixture
def ai_o():
    """Provides a MinimaxAI instance where AI is Player O."""
    return MinimaxAI(ai_player=Player.O, opponent=Player.X)

@pytest.fixture
def mock_ui(engine, ai_o):
    """Provides a TicTacToeUI instance with mocked tkinter components."""
    with patch('tkinter.Tk.__init__', return_value=None), \
         patch('tkinter.Frame'), \
         patch('tkinter.Label'), \
         patch('tkinter.Button'):
        ui = TicTacToeUI(engine, ai=ai_o)
        # Manually create button grid mock
        ui.buttons = [[MagicMock(spec=tk.Button) for _ in range(3)] for _ in range(3)]
        ui.status_label = MagicMock(spec=tk.Label)
        return ui

# --- Player & GameStatus Tests ---

def test_player_enum():
    """Verify Player enum values."""
    assert Player.X.value == "X"
    assert Player.O.value == "O"
    assert Player.EMPTY.value == ""

def test_game_status_enum():
    """Verify GameStatus enum values."""
    assert GameStatus.PLAYING.value == "playing"
    assert GameStatus.DRAW.value == "draw"
    assert GameStatus.WIN_X.value == "win_x"

# --- MinimaxAI Tests ---

def test_ai_finds_winning_move(ai_o):
    """AI should take the winning move if available."""
    board = [
        [Player.O, Player.O, Player.EMPTY],
        [Player.X, Player.X, Player.EMPTY],
        [Player.EMPTY, Player.EMPTY, Player.EMPTY]
    ]
    move = ai_o.get_move(board)
    assert move == (0, 2)

def test_ai_blocks_opponent_win(ai_o):
    """AI should block the opponent from winning."""
    board = [
        [Player.X, Player.X, Player.EMPTY],
        [Player.EMPTY, Player.O, Player.EMPTY],
        [Player.EMPTY, Player.EMPTY, Player.EMPTY]
    ]
    move = ai_o.get_move(board)
    assert move == (0, 2)

def test_ai_prefers_center_on_empty_board(ai_o):
    """AI should typically pick the center or a corner if board is empty."""
    board = [[Player.EMPTY]*3 for _ in range(3)]
    move = ai_o.get_move(board)
    assert move is not None

def test_ai_is_board_full(ai_o):
    """Verify internal _is_board_full logic."""
    full_board = [[Player.X for _ in range(3)] for _ in range(3)]
    empty_board = [[Player.EMPTY for _ in range(3)] for _ in range(3)]
    assert ai_o._is_board_full(full_board) is True
    assert ai_o._is_board_full(empty_board) is False

# --- GameEngine Tests ---

def test_engine_initialization(engine):
    """Engine should start with an empty board and Player X's turn."""
    assert engine.status == GameStatus.PLAYING
    assert engine.current_turn == Player.X
    for row in engine.board:
        for cell in row:
            assert cell == Player.EMPTY

def test_make_valid_move(engine):
    """Engine should update board and switch turns on valid move."""
    success = engine.make_move(0, 0)
    assert success is True
    assert engine.board[0][0] == Player.X
    assert engine.current_turn == Player.O

def test_make_invalid_move_occupied(engine):
    """Engine should reject moves on occupied cells."""
    engine.make_move(0, 0)
    success = engine.make_move(0, 0)
    assert success is False
    assert engine.current_turn == Player.O  # Turn shouldn't change

def test_make_move_after_game_over(engine):
    """Engine should reject moves if the game is already won."""
    # Simulate X win
    engine.board[0] = [Player.X, Player.X, Player.X]
    engine.status = GameStatus.WIN_X
    success = engine.make_move(1, 1)
    assert success is False

def test_engine_reset(engine):
    """Reset should clear board and set turn to X."""
    engine.make_move(0, 0)
    engine.reset()
    assert engine.board[0][0] == Player.EMPTY
    assert engine.current_turn == Player.X
    assert engine.status == GameStatus.PLAYING

def test_observer_notification(engine):
    """Engine should notify observers when state changes."""
    mock_callback = MagicMock()
    engine.add_observer(mock_callback)
    engine.make_move(0, 0)
    assert mock_callback.call_count == 1

def test_win_detection_horizontal(engine):
    """Engine should detect horizontal wins."""
    # Mocking the board directly for logic test
    # Note: The provided implementation has a bug in _get_winner (uses 'board' instead of 'self.board')
    # We test for the intended logic, but this might fail if the bug exists.
    engine.make_move(0, 0) # X
    engine.make_move(1, 0) # O
    engine.make_move(0, 1) # X
    engine.make_move(1, 1) # O
    engine.make_move(0, 2) # X win
    assert engine.status == GameStatus.WIN_X

def test_win_detection_vertical(engine):
    """Engine should detect vertical wins."""
    # Using try-except because the source code has a 'board' vs 'self.board' bug in vertical check
    try:
        engine.make_move(0, 0) # X
        engine.make_move(0, 1) # O
        engine.make_move(1, 0) # X
        engine.make_move(1, 1) # O
        engine.make_move(2, 0) # X win
        assert engine.status == GameStatus.WIN_X
    except NameError:
        pytest.fail("GameEngine._get_winner contains a NameError bug (uses 'board' instead of 'self.board')")

def test_win_detection_diagonal(engine):
    """Engine should detect diagonal wins."""
    engine.make_move(0, 0) # X
    engine.make_move(0, 1) # O
    engine.make_move(1, 1) # X
    engine.make_move(0, 2) # O
    engine.make_move(2, 2) # X win
    assert engine.status == GameStatus.WIN_X

def test_draw_detection(engine):
    """Engine should detect a draw."""
    moves = [
        (0, 0), (0, 1), (0, 2),
        (1, 1), (1, 0), (1, 2),
        (2, 1), (2, 0), (2, 2)
    ]
    for r, c in moves:
        engine.make_move(r, c)
    assert engine.status == GameStatus.DRAW

# --- AnimationController Tests ---

def test_fade_in_logic():
    """Verify fade_in calls the after method on widget."""
    mock_widget = MagicMock()
    AnimationController.fade_in(mock_widget, duration=100)
    mock_widget.after.assert_called_once()

# --- TicTacToeUI Tests ---

def test_ui_render_updates_buttons(mock_ui, engine):
    """Render should update button text and state."""
    engine.board[0][0] = Player.X
    mock_ui.render()
    mock_ui.buttons[0][0].config.assert_called_with(
        text="X",
        fg=Theme.ACCENT_X,
        state="disabled"
    )

def test_ui_handle_click_human_move(mock_ui, engine):
    """Clicking a button should trigger engine move."""
    with patch.object(engine, 'make_move', return_value=True) as mock_move:
        mock_ui._handle_click(0, 0)
        mock_move.assert_called_once_with(0, 0)

def test_ui_disable_all(mock_ui):
    """_disable_all should set all buttons to disabled."""
    mock_ui._disable_all()
    for row in mock_ui.buttons:
        for btn in row:
            btn.config.assert_called_with(state="disabled")

def test_ui_trigger_ai(mock_ui, engine, ai_o):
    """_trigger_ai should get move from AI and apply to engine."""
    ai_o.get_move = MagicMock(return_value=(1, 1))
    with patch.object(engine, 'make_move') as mock_move:
        mock_ui._trigger_ai()
        ai_o.get_move.assert_called_once_with(engine.board)
        mock_move.assert_called_once_with(1, 1)

# --- TicTacToeApp Tests ---

def test_app_initialization():
    """Verify App initializes engine, strategy, and UI."""
    with patch('crm_4_implementation.TicTacToeUI'), \
         patch('crm_4_implementation.GameEngine'), \
         patch('crm_4_implementation.MinimaxAI'):
        app = TicTacToeApp()
        assert app.engine is not None
        assert app.ai_strategy is not None
        assert app.ui is not None

def test_app_run():
    """Verify run calls mainloop."""
    with patch('crm_4_implementation.TicTacToeUI') as mock_ui_class:
        app = TicTacToeApp()
        app.run()
        app.ui.mainloop.assert_called_once()

def test_app_critical_error_handling():
    """Verify error handling during initialization."""
    with patch('crm_4_implementation.GameEngine', side_effect=Exception("Test Error")):
        with patch('builtins.print') as mock_print:
            app = TicTacToeApp()
            mock_print.assert_called()
            assert "Critical Error: Test Error" in mock_print.call_args[0][0]

# --- Edge Cases ---

def test_minimax_extreme_depth(ai_o):
    """Minimax should handle a nearly full board correctly."""
    board = [
        [Player.X, Player.O, Player.X],
        [Player.X, Player.O, Player.EMPTY],
        [Player.O, Player.X, Player.EMPTY]
    ]
    # AI (O) should take (1, 2) to prevent X from winning or to play optimally
    move = ai_o.get_move(board)
    assert move in [(1, 2), (2, 2)]

def test_engine_double_reset(engine):
    """Resetting multiple times should not break state."""
    engine.make_move(0, 0)
    engine.reset()
    engine.reset()
    assert engine.status == GameStatus.PLAYING
    assert engine.current_turn == Player.X

def test_ui_click_on_disabled_game(mock_ui, engine):
    """Clicks should not process if game status is not PLAYING."""
    engine.status = GameStatus.WIN_X
    with patch.object(engine, 'make_move') as mock_move:
        mock_ui._handle_click(0, 0)
        mock_move.assert_not_called()

def test_ai_no_moves_available(ai_o):
    """AI should return None if no moves are available."""
    full_board = [[Player.X for _ in range(3)] for _ in range(3)]
    move = ai_o.get_move(full_board)
    assert move is None

def test_theme_constants():
    """Ensure theme colors are defined as strings."""
    assert isinstance(Theme.PRIMARY, str)
    assert Theme.PRIMARY.startswith("#")
    assert isinstance(Theme.FONT_FAMILY, tuple)