import pytest
from unittest.mock import patch
from crm_5_implementation import (
    Player,
    GameStatus,
    TicTacToeGame,
    GameRenderer,
    GameEngine
)


@pytest.fixture
def tic_tac_toe_game():
    """Fixture to create a fresh TicTacToeGame instance."""
    return TicTacToeGame()


@pytest.fixture
def game_renderer():
    """Fixture to create a fresh GameRenderer instance."""
    return GameRenderer()


@pytest.fixture
def game_engine():
    """Fixture to create a fresh GameEngine instance."""
    return GameEngine()


class TestPlayerEnum:
    """Test Player enumeration values."""
    
    def test_player_enum_values(self):
        """Test that Player enum has correct values."""
        assert Player.X.value == "X"
        assert Player.O.value == "O"
        assert Player.EMPTY.value == " "


class TestGameStatusEnum:
    """Test GameStatus enumeration values."""
    
    def test_game_status_enum_values(self):
        """Test that GameStatus enum has correct values."""
        assert GameStatus.PLAYING.value == "playing"
        assert GameStatus.X_WON.value == "x_won"
        assert GameStatus.O_WON.value == "o_won"
        assert GameStatus.DRAW.value == "draw"


class TestTicTacToeGame:
    """Test TicTacToeGame class functionality."""
    
    def test_initialization(self, tic_tac_toe_game):
        """Test game initialization."""
        assert tic_tac_toe_game.board == [
            [Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY]
        ]
        assert tic_tac_toe_game.current_player == Player.X
        assert tic_tac_toe_game.game_status == GameStatus.PLAYING
        assert tic_tac_toe_game.move_history == []
    
    def test_make_move_valid(self, tic_tac_toe_game):
        """Test making a valid move."""
        result = tic_tac_toe_game.make_move(0, 0)
        assert result is True
        assert tic_tac_toe_game.board[0][0] == Player.X
        assert tic_tac_toe_game.current_player == Player.O
        assert tic_tac_toe_game.move_history == [(0, 0)]
    
    def test_make_move_invalid_coordinates(self, tic_tac_toe_game):
        """Test making a move with invalid coordinates."""
        with pytest.raises(ValueError):
            tic_tac_toe_game.make_move(-1, 0)
        
        with pytest.raises(ValueError):
            tic_tac_toe_game.make_move(0, 3)
    
    def test_make_move_occupied_cell(self, tic_tac_toe_game):
        """Test making a move on an occupied cell."""
        # Make first move
        tic_tac_toe_game.make_move(0, 0)
        
        # Try to make move on same cell
        result = tic_tac_toe_game.make_move(0, 0)
        assert result is False
        assert tic_tac_toe_game.board[0][0] == Player.X
    
    def test_check_game_status_x_wins_row(self, tic_tac_toe_game):
        """Test checking game status when X wins by row."""
        # Make moves for X to win in first row
        tic_tac_toe_game.make_move(0, 0)  # X
        tic_tac_toe_game.make_move(1, 0)  # O
        tic_tac_toe_game.make_move(0, 1)  # X
        tic_tac_toe_game.make_move(1, 1)  # O
        tic_tac_toe_game.make_move(0, 2)  # X
        
        assert tic_tac_toe_game.game_status == GameStatus.X_WON
    
    def test_check_game_status_o_wins_column(self, tic_tac_toe_game):
        """Test checking game status when O wins by column."""
        # Make moves for O to win in first column
        tic_tac_toe_game.make_move(0, 0)  # X
        tic_tac_toe_game.make_move(1, 0)  # O
        tic_tac_toe_game.make_move(0, 1)  # X
        tic_tac_toe_game.make_move(2, 0)  # O
        tic_tac_toe_game.make_move(0, 2)  # X
        tic_tac_toe_game.make_move(1, 1)  # O
        
        assert tic_tac_toe_game.game_status == GameStatus.O_WON
    
    def test_check_game_status_x_wins_diagonal(self, tic_tac_toe_game):
        """Test checking game status when X wins by diagonal."""
        # Make moves for X to win in main diagonal
        tic_tac_toe_game.make_move(0, 0)  # X
        tic_tac_toe_game.make_move(1, 0)  # O
        tic_tac_toe_game.make_move(1, 1)  # X
        tic_tac_toe_game.make_move(0, 2)  # O
        tic_tac_toe_game.make_move(2, 2)  # X
        
        assert tic_tac_toe_game.game_status == GameStatus.X_WON
    
    def test_check_game_status_draw(self, tic_tac_toe_game):
        """Test checking game status when game is a draw."""
        # Fill board with alternating moves to create draw
        moves = [
            (0, 0), (1, 1), (0, 1), (1, 0), (0, 2),
            (2, 0), (2, 1), (2, 2), (1, 2)
        ]
        
        for i, move in enumerate(moves):
            if i % 2 == 0:
                tic_tac_toe_game.make_move(move[0], move[1])  # X
            else:
                tic_tac_toe_game.make_move(move[0], move[1])  # O
        
        assert tic_tac_toe_game.game_status == GameStatus.DRAW
    
    def test_reset_game(self, tic_tac_toe_game):
        """Test resetting the game."""
        # Make some moves
        tic_tac_toe_game.make_move(0, 0)
        tic_tac_toe_game.make_move(1, 1)
        
        # Reset game
        tic_tac_toe_game.reset_game()
        
        assert tic_tac_toe_game.board == [
            [Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY]
        ]
        assert tic_tac_toe_game.current_player == Player.X
        assert tic_tac_toe_game.game_status == GameStatus.PLAYING
        assert tic_tac_toe_game.move_history == []
    
    def test_get_board_state(self, tic_tac_toe_game):
        """Test getting board state."""
        # Make a move
        tic_tac_toe_game.make_move(0, 0)
        
        board_state = tic_tac_toe_game.get_board_state()
        assert board_state[0][0] == Player.X
        assert board_state[1][0] == Player.EMPTY
    
    def test_get_current_player(self, tic_tac_toe_game):
        """Test getting current player."""
        assert tic_tac_toe_game.get_current_player() == Player.X
        
        # Make a move
        tic_tac_toe_game.make_move(0, 0)
        assert tic_tac_toe_game.get_current_player() == Player.O
    
    def test_get_game_status(self, tic_tac_toe_game):
        """Test getting game status."""
        assert tic_tac_toe_game.get_game_status() == GameStatus.PLAYING
        
        # Make moves to win
        tic_tac_toe_game.make_move(0, 0)
        tic_tac_toe_game.make_move(1, 0)
        tic_tac_toe_game.make_move(0, 1)
        tic_tac_toe_game.make_move(1, 1)
        tic_tac_toe_game.make_move(0, 2)
        
        assert tic_tac_toe_game.get_game_status() == GameStatus.X_WON
    
    def test_get_move_history(self, tic_tac_toe_game):
        """Test getting move history."""
        # Make some moves
        tic_tac_toe_game.make_move(0, 0)
        tic_tac_toe_game.make_move(1, 1)
        
        history = tic_tac_toe_game.get_move_history()
        assert history == [(0, 0), (1, 1)]
    
    def test_get_winner(self, tic_tac_toe_game):
        """Test getting winner."""
        assert tic_tac_toe_game.get_winner() is None
        
        # Make moves to win
        tic_tac_toe_game.make_move(0, 0)
        tic_tac_toe_game.make_move(1, 0)
        tic_tac_toe_game.make_move(0, 1)
        tic_tac_toe_game.make_move(1, 1)
        tic_tac_toe_game.make_move(0, 2)
        
        assert tic_tac_toe_game.get_winner() == Player.X
    
    def test_get_game_state(self, tic_tac_toe_game):
        """Test getting complete game state."""
        state = tic_tac_toe_game.get_game_state()
        
        assert state["board"] == [
            [Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY]
        ]
        assert state["current_player"] == "X"
        assert state["game_status"] == "playing"
        assert state["winner"] is None
        assert state["move_history"] == []


class TestGameRenderer:
    """Test GameRenderer class functionality."""
    
    def test_initialization(self, game_renderer):
        """Test renderer initialization."""
        assert game_renderer.game_state is None
    
    def test_render_html(self, game_renderer, tic_tac_toe_game):
        """Test rendering HTML."""
        html_content = game_renderer.render_html(tic_tac_toe_game)
        
        assert "Tic Tac Toe" in html_content
        assert "Current Player: X" in html_content
        assert '<div class="cell"' in html_content
    
    def test_render_board(self, game_renderer, tic_tac_toe_game):
        """Test rendering board HTML."""
        board_html = game_renderer._render_board(tic_tac_toe_game)
        
        assert '<div class="cell"' in board_html
        assert 'data-row="0" data-col="0"' in board_html


class TestGameEngine:
    """Test GameEngine class functionality."""
    
    def test_engine_initialization(self, game_engine):
        """Test engine initialization."""
        assert isinstance(game_engine.game, TicTacToeGame)
        assert isinstance(game_engine.renderer, GameRenderer)
    
    def test_play_move_valid(self, game_engine):
        """Test playing a valid move."""
        result = game_engine.play_move(0, 0)
        
        assert result["success"] is True
        assert result["state"]["game_status"] == "playing"
        assert result["state"]["current_player"] == "O"
    
    def test_play_move_invalid(self, game_engine):
        """Test playing an invalid move."""
        # Make first move
        game_engine.play_move(0, 0)
        
        # Try to make move on occupied cell
        result = game_engine.play_move(0, 0)
        
        assert result["success"] is False
        assert "Invalid move" in result["error"]
    
    def test_play_move_invalid_coordinates(self, game_engine):
        """Test playing move with invalid coordinates."""
        result = game_engine.play_move(-1, 0)
        
        assert result["success"] is False
        assert "Invalid move" in result["error"]
    
    def test_reset(self, game_engine):
        """Test resetting the game."""
        # Make some moves
        game_engine.play_move(0, 0)
        
        reset_result = game_engine.reset()
        
        assert reset_result["success"] is True
        assert reset_result["state"]["game_status"] == "playing"
        assert reset_result["state"]["current_player"] == "X"
    
    def test_get_html(self, game_engine):
        """Test getting HTML."""
        html_content = game_engine.get_html()
        
        assert "Tic Tac Toe" in html_content
        assert '<div class="cell"' in html_content
    
    def test_get_game_state(self, game_engine):
        """Test getting game state."""
        state = game_engine.get_game_state()
        
        assert state["game_status"] == "playing"
        assert state["current_player"] == "X"


def test_create_sample_game():
    """Test creating a sample game."""
    from crm_5_implementation import create_sample_game
    
    engine = create_sample_game()
    assert isinstance(engine, GameEngine)


def test_test_game_logic():
    """Test the game logic testing function."""
    from crm_5_implementation import test_game_logic
    
    # Just make sure it runs without errors
    try:
        test_game_logic()
        assert True
    except Exception:
        pytest.fail("test_game_logic function should not raise an exception")
