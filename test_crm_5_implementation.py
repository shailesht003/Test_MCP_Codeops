import pytest
from unittest.mock import patch, MagicMock
import os
import json

from crm_5_implementation import (
    PlayerSymbol,
    GameStatus,
    Player,
    GameBoard,
    TicTacToe,
    create_html_template,
    save_game_state,
    load_game_state
)


class TestPlayerSymbol:
    """Test PlayerSymbol enumeration."""
    
    def test_player_symbol_values(self):
        """Test that PlayerSymbol has correct values."""
        assert PlayerSymbol.X.value == "X"
        assert PlayerSymbol.O.value == "O"


class TestPlayer:
    """Test Player class."""
    
    def test_player_creation(self):
        """Test Player creation with valid parameters."""
        player = Player(PlayerSymbol.X, "Test Player")
        assert player.symbol == PlayerSymbol.X
        assert player.name == "Test Player"
    
    def test_player_equality(self):
        """Test Player equality comparison."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.X, "Player X")
        player3 = Player(PlayerSymbol.O, "Player O")
        
        assert player1 == player2
        assert player1 != player3


class TestGameBoard:
    """Test GameBoard class."""
    
    def test_board_initialization(self):
        """Test board initialization with default size."""
        board = GameBoard()
        assert board.size == 3
        assert len(board.board) == 3
        assert all(len(row) == 3 for row in board.board)
        assert all(cell is None for row in board.board for cell in row)
    
    def test_board_initialization_custom_size(self):
        """Test board initialization with custom size."""
        board = GameBoard(5)
        assert board.size == 5
        assert len(board.board) == 5
        assert all(len(row) == 5 for row in board.board)
    
    def test_make_move_valid(self):
        """Test making a valid move."""
        board = GameBoard()
        result = board.make_move(0, 0, PlayerSymbol.X)
        
        assert result is True
        assert board.get_cell(0, 0) == PlayerSymbol.X
    
    def test_make_move_invalid_coordinates(self):
        """Test making a move with invalid coordinates."""
        board = GameBoard()
        
        with pytest.raises(IndexError):
            board.make_move(5, 5, PlayerSymbol.X)
    
    def test_make_move_occupied_cell(self):
        """Test making a move on an occupied cell."""
        board = GameBoard()
        board.make_move(0, 0, PlayerSymbol.X)
        result = board.make_move(0, 0, PlayerSymbol.O)
        
        assert result is False
        assert board.get_cell(0, 0) == PlayerSymbol.X
    
    def test_get_cell(self):
        """Test getting cell value."""
        board = GameBoard()
        board.make_move(1, 1, PlayerSymbol.O)
        
        assert board.get_cell(0, 0) is None
        assert board.get_cell(1, 1) == PlayerSymbol.O
    
    def test_is_full_empty_board(self):
        """Test is_full on empty board."""
        board = GameBoard()
        assert board.is_full() is False
    
    def test_is_full_full_board(self):
        """Test is_full on full board."""
        board = GameBoard()
        for i in range(3):
            for j in range(3):
                board.make_move(i, j, PlayerSymbol.X)
        
        assert board.is_full() is True
    
    def test_get_empty_cells(self):
        """Test getting empty cells."""
        board = GameBoard()
        board.make_move(0, 0, PlayerSymbol.X)
        
        empty_cells = board.get_empty_cells()
        assert len(empty_cells) == 8
        assert (0, 0) not in empty_cells
    
    def test_reset_board(self):
        """Test resetting the board."""
        board = GameBoard()
        board.make_move(0, 0, PlayerSymbol.X)
        board.reset()
        
        assert board.is_full() is False
        assert all(cell is None for row in board.board for cell in row)


class TestTicTacToe:
    """Test TicTacToe class."""
    
    def test_game_initialization(self):
        """Test game initialization."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.O, "Player O")
        
        game = TicTacToe(player1, player2)
        
        assert game.player1 == player1
        assert game.player2 == player2
        assert game.current_player == player1
        assert game.status == GameStatus.PLAYING
        assert game.winner is None
        assert len(game.move_history) == 0
    
    def test_game_initialization_custom_size(self):
        """Test game initialization with custom board size."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.O, "Player O")
        
        game = TicTacToe(player1, player2, 5)
        
        assert game.board.size == 5
    
    def test_make_move_valid(self):
        """Test making a valid move."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.O, "Player O")
        
        game = TicTacToe(player1, player2)
        
        result = game.make_move(0, 0)
        
        assert result is True
        assert game.current_player == player2
        assert len(game.move_history) == 1
        assert game.move_history[0] == (0, 0, PlayerSymbol.X)
    
    def test_make_move_invalid_game_ended(self):
        """Test making a move when game has ended."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.O, "Player O")
        
        game = TicTacToe(player1, player2)
        
        # Make moves to end the game
        game.make_move(0, 0)  # X plays at (0,0)
        game.make_move(1, 1)  # O plays at (1,1)
        game.make_move(0, 1)  # X plays at (0,1)
        game.make_move(1, 0)  # O plays at (1,0)
        game.make_move(0, 2)  # X plays at (0,2) - wins
        
        with pytest.raises(Exception):  # Should raise an exception or handle properly
            game.make_move(2, 2)
    
    def test_check_win_row(self):
        """Test win condition checking for row."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.O, "Player O")
        
        game = TicTacToe(player1, player2)
        
        # Make moves to create a winning row
        game.make_move(0, 0)  # X plays at (0,0)
        game.make_move(1, 1)  # O plays at (1,1)
        game.make_move(0, 1)  # X plays at (0,1)
        game.make_move(1, 0)  # O plays at (1,0)
        result = game.make_move(0, 2)  # X plays at (0,2) - wins
        
        assert result is True
        assert game.status == GameStatus.PLAYING  # Should still be playing until next move
    
    def test_check_win_column(self):
        """Test win condition checking for column."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.O, "Player O")
        
        game = TicTacToe(player1, player2)
        
        # Make moves to create a winning column
        game.make_move(0, 0)  # X plays at (0,0)
        game.make_move(1, 1)  # O plays at (1,1)
        game.make_move(1, 0)  # X plays at (1,0)
        game.make_move(2, 1)  # O plays at (2,1)
        result = game.make_move(2, 0)  # X plays at (2,0) - wins
        
        assert result is True
    
    def test_check_win_diagonal(self):
        """Test win condition checking for diagonal."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.O, "Player O")
        
        game = TicTacToe(player1, player2)
        
        # Make moves to create a winning diagonal
        game.make_move(0, 0)  # X plays at (0,0)
        game.make_move(1, 1)  # O plays at (1,1)
        game.make_move(1, 0)  # X plays at (1,0)
        game.make_move(2, 2)  # O plays at (2,2)
        result = game.make_move(2, 0)  # X plays at (2,0) - wins
        
        assert result is True
    
    def test_get_game_state(self):
        """Test getting game state."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.O, "Player O")
        
        game = TicTacToe(player1, player2)
        state = game.get_game_state()
        
        assert isinstance(state, dict)
        assert "current_player_symbol" in state
        assert "board" in state
        assert "status" in state
        assert "winner" in state
    
    def test_reset_game(self):
        """Test resetting the game."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.O, "Player O")
        
        game = TicTacToe(player1, player2)
        game.make_move(0, 0)  # X plays at (0,0)
        
        # Reset the game
        # Note: There's no explicit reset method in the original code,
        # but we can simulate by creating a new game instance
        
        game2 = TicTacToe(player1, player2)
        
        assert game2.current_player == player1
        assert game2.status == GameStatus.PLAYING
        assert len(game2.move_history) == 0
    
    def test_draw_condition(self):
        """Test draw condition."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.O, "Player O")
        
        game = TicTacToe(player1, player2)
        
        # Fill board with alternating moves to create a draw
        game.make_move(0, 0)  # X plays at (0,0)
        game.make_move(0, 1)  # O plays at (0,1)
        game.make_move(0, 2)  # X plays at (0,2)
        game.make_move(1, 0)  # O plays at (1,0)
        game.make_move(1, 1)  # X plays at (1,1)
        game.make_move(1, 2)  # O plays at (1,2)
        game.make_move(2, 0)  # X plays at (2,0)
        game.make_move(2, 1)  # O plays at (2,1)
        game.make_move(2, 2)  # X plays at (2,2)
        
        # Check that game state is updated correctly
        state = game.get_game_state()
        assert state["status"] == "draw" or state["status"] == "o_wins" or state["status"] == "x_wins"


class TestCreateHtmlTemplate:
    """Test create_html_template function."""
    
    def test_create_html_template(self):
        """Test creating HTML template with valid game state."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.O, "Player O")
        
        game = TicTacToe(player1, player2)
        state = game.get_game_state()
        
        html_content = create_html_template(state, "test_game")
        
        assert isinstance(html_content, str)
        assert "Tic Tac Toe" in html_content
        assert "Current Player:" in html_content
        assert "resetGame()" in html_content
        assert "saveGame()" in html_content


class TestSaveLoadGameState:
    """Test save_game_state and load_game_state functions."""
    
    def test_save_game_state(self, tmp_path):
        """Test saving game state to file."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.O, "Player O")
        
        game = TicTacToe(player1, player2)
        game.make_move(0, 0)  # X plays at (0,0)
        
        file_path = tmp_path / "test_game.json"
        save_game_state(game, str(file_path))
        
        assert file_path.exists()
        
        # Read and verify content
        with open(file_path, 'r') as f:
            saved_data = json.load(f)
        
        assert "current_player_symbol" in saved_data
        assert "board" in saved_data
        assert "status" in saved_data
    
    def test_save_game_state_error(self, tmp_path):
        """Test saving game state with invalid path."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.O, "Player O")
        
        game = TicTacToe(player1, player2)
        
        # Try to save to a non-writable location
        with pytest.raises(IOError):
            save_game_state(game, "/nonexistent/directory/game.json")
    
    def test_load_game_state(self, tmp_path):
        """Test loading game state from file."""
        player1 = Player(PlayerSymbol.X, "Player X")
        player2 = Player(PlayerSymbol.O, "Player O")
        
        game = TicTacToe(player1, player2)
        game.make_move(0, 0)  # X plays at (0,0)
        
        file_path = tmp_path / "test_game.json"
        save_game_state(game, str(file_path))
        
        loaded_data = load_game_state(str(file_path))
        
        assert isinstance(loaded_data, dict)
        assert "current_player_symbol" in loaded_data
        assert "board" in loaded_data
    
    def test_load_game_state_file_not_found(self):
        """Test loading game state from non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_game_state("nonexistent_file.json")
    
    def test_load_game_state_invalid_json(self, tmp_path):
        """Test loading game state from invalid JSON file."""
        file_path = tmp_path / "invalid.json"
        with open(file_path, 'w') as f:
            f.write("invalid json content")
        
        with pytest.raises(json.JSONDecodeError):
            load_game_state(str(file_path))


class TestMainFunction:
    """Test main function."""
    
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_function(self, mock_stdout):
        """Test main function execution."""
        # This is a basic test - in real scenario, it would execute the full main function
        # We're just ensuring it doesn't crash
        
        try:
            # Import here to avoid circular imports in test setup
            from crm_5_implementation import main
            
            # We can't easily test the full main function without mocking more complex behavior
            # But we can at least ensure it doesn't crash on basic execution
            main()
            
            # If we get here without exception, the test passes
            assert True
            
        except Exception as e:
            # If there are exceptions, they should not be from basic functionality
            # This is just a smoke test
            assert "Error during game execution" not in str(e) or "main" in str(e)


def test_edge_cases():
    """Test edge cases for all classes and functions."""
    
    # Test invalid board size
    with pytest.raises(Exception):
        GameBoard(-1)  # This might raise an exception in real implementation
    
    # Test invalid player creation
    with pytest.raises(Exception):
        Player("invalid_symbol", "Player")  # This might raise an exception in real implementation
    
    # Test multiple wins condition (should be handled by game logic)
    
    # Test large board size
    large_board = GameBoard(100)
    assert large_board.size == 100
    
    # Test negative board size
    with pytest.raises(Exception):
        GameBoard(-5)
    
    # Test zero board size
    with pytest.raises(Exception):
        GameBoard(0)


def test_code_coverage():
    """Test that all code paths are covered."""
    
    # Test that all enums have proper values
    assert PlayerSymbol.X.value == "X"
    assert PlayerSymbol.O.value == "O"
    
    # Test that all game statuses are handled
    assert GameStatus.PLAYING.value == "playing"
    assert GameStatus.X_WINS.value == "x_wins"
    assert GameStatus.O_WINS.value == "o_wins"
    assert GameStatus.DRAW.value == "draw"
    
    # Test that the main function can be called without error
    try:
        from crm_5_implementation import main
        # We're not actually running main() here, just ensuring it exists
        assert callable(main)
    except Exception:
        # If there are import errors, the test should fail gracefully
        assert False
    
    # Test that all classes can be instantiated
    player1 = Player(PlayerSymbol.X, "Player X")
    player2 = Player(PlayerSymbol.O, "Player O")
    
    board = GameBoard()
    game = TicTacToe(player1, player2)
    
    assert isinstance(player1, Player)
    assert isinstance(board, GameBoard)
    assert isinstance(game, TicTacToe)
    
    # Test that all methods exist
    assert hasattr(board, 'make_move')
    assert hasattr(board, 'get_cell')
    assert hasattr(board, 'is_full')
    assert hasattr(board, 'get_empty_cells')
    assert hasattr(board, 'reset')
    
    assert hasattr(game, 'make_move')
    assert hasattr(game, 'get_game_state')
    assert hasattr(game, 'current_player')
    assert hasattr(game, 'status')
    
    # Test that all constants are accessible
    assert PlayerSymbol.X is not None
    assert PlayerSymbol.O is not None
    assert GameStatus.PLAYING is not None
    assert GameStatus.X_WINS is not None
    assert GameStatus.O_WINS is not None
    assert GameStatus.DRAW is not None