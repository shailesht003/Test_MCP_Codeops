import pytest
import tkinter as tk
from unittest.mock import patch, MagicMock
from crm_4_implementation import (
    TicTacToeGame, 
    GameEngine, 
    Player, 
    CellState, 
    GameState,
    AIPlayer,
    HumanPlayer
)

@pytest.fixture
def root():
    """Provides a fresh Tkinter root instance for each test."""
    root = tk.Tk()
    yield root
    root.destroy()

@pytest.fixture
def game_instance(root):
    """Provides an initialized instance of the TicTacToeGame UI and Engine."""
    app = TicTacToeGame(root)
    return app

class TestTicTacToeIntegration:
    """Integration tests for the Tic Tac Toe system components."""

    def test_initialization_state(self, game_instance):
        """Tests that the UI and Engine are correctly synchronized upon startup."""
        assert game_instance.engine.current_state == GameState.PLAYING
        assert len(game_instance.buttons) == 9
        for btn in game_instance.buttons:
            assert btn["text"] == ""
            assert btn["state"] == tk.NORMAL

    def test_human_move_updates_ui_and_engine(self, game_instance):
        """Tests that clicking a button updates both the logic engine and the UI text."""
        # Simulate clicking the center cell (index 4)
        center_button = game_instance.buttons[4]
        
        # Manually trigger the command associated with the button
        game_instance.handle_click(4)
        
        # Check Engine State
        assert game_instance.engine.board[4] != CellState.EMPTY
        
        # Check UI State
        assert center_button["text"] in ["X", "O"]
        assert center_button["state"] == tk.DISABLED

    @patch('tkinter.messagebox.showinfo')
    def test_win_condition_integration(self, mock_showinfo, game_instance):
        """Tests a full sequence of moves leading to a win and UI notification."""
        # Setup engine for a quick win for 'X' on top row
        # X: 0, 1, 2
        # O: 3, 4
        moves = [0, 3, 1, 4, 2]
        
        for move in moves:
            game_instance.handle_click(move)
            
        assert game_instance.engine.current_state == GameState.WIN
        assert mock_showinfo.called
        assert "Winner" in mock_showinfo.call_args[0][0] or "Winner" in mock_showinfo.call_args[0][1]

    def test_ai_integration_after_human_move(self, game_instance):
        """Tests that the AI automatically moves after a human player makes a move."""
        # Ensure the game is set to Human vs AI
        game_instance.set_player_mode("PvE")
        
        # Human moves
        game_instance.handle_click(0)
        
        # Force UI update to process any pending events/after() calls
        game_instance.root.update()
        
        # Count non-empty cells
        filled_cells = [c for c in game_instance.engine.board if c != CellState.EMPTY]
        
        # Should be 2: one from human, one from AI
        assert len(filled_cells) == 2

    def test_reset_functionality(self, game_instance):
        """Tests that the reset button clears both engine and UI states."""
        # Make some moves
        game_instance.handle_click(0)
        game_instance.handle_click(1)
        
        # Trigger Reset
        game_instance.reset_game()
        
        # Verify Engine
        assert all(cell == CellState.EMPTY for cell in game_instance.engine.board)
        assert game_instance.engine.current_state == GameState.PLAYING
        
        # Verify UI
        for btn in game_instance.buttons:
            assert btn["text"] == ""
            assert btn["state"] == tk.NORMAL

    @patch('tkinter.messagebox.showinfo')
    def test_draw_condition_integration(self, mock_showinfo, game_instance):
        """Tests that a full board with no winner results in a DRAW state."""
        # Sequence for a draw:
        # X O X
        # X O O
        # O X X
        draw_moves = [0, 1, 2, 4, 3, 5, 7, 6, 8]
        
        for move in draw_moves:
            game_instance.handle_click(move)
            
        assert game_instance.engine.current_state == GameState.DRAW
        assert mock_showinfo.called
        assert "Draw" in mock_showinfo.call_args[0][1]

    def test_theme_application_on_ui_components(self, game_instance):
        """Tests that the Theme constants are correctly applied to UI widgets."""
        from crm_4_implementation import Theme
        
        # Check background of the main container
        assert game_instance.main_frame.cget("bg") == Theme.BACKGROUND
        
        # Check if buttons use the surface color
        assert game_instance.buttons[0].cget("bg") == Theme.SURFACE

    def test_invalid_move_prevention(self, game_instance):
        """Tests that clicking an already occupied cell does not change the engine state."""
        game_instance.handle_click(0)
        first_player = game_instance.engine.board[0]
        
        # Try clicking the same cell again
        game_instance.handle_click(0)
        
        # Ensure it's still the same player's mark and engine didn't crash
        assert game_instance.engine.board[0] == first_player
        # Ensure turn didn't advance (next move should still be valid elsewhere)
        assert game_instance.engine.turn_count == 1

    def test_player_switching_logic(self, game_instance):
        """Tests that the engine correctly toggles between Player X and Player O."""
        initial_player = game_instance.engine.current_player
        
        game_instance.handle_click(0)
        second_player = game_instance.engine.current_player
        
        assert initial_player != second_player
        
        game_instance.handle_click(1)
        third_player = game_instance.engine.current_player
        
        assert third_player == initial_player

    def test_score_tracking_integration(self, game_instance):
        """Tests that winning a game updates the score tracking component."""
        initial_score_x = game_instance.scores['X']
        
        # Simulate X winning
        # X: 0, 1, 2
        # O: 3, 4
        moves = [0, 3, 1, 4, 2]
        with patch('tkinter.messagebox.showinfo'):
            for move in moves:
                game_instance.handle_click(move)
                
        assert game_instance.scores['X'] == initial_score_x + 1
        assert "1" in game_instance.score_labels['X'].cget("text")

def test_ai_difficulty_minimax_integration(root):
    """Tests that the AI uses Minimax logic to block an immediate win."""
    app = TicTacToeGame(root)
    app.set_player_mode("PvE")
    app.engine.difficulty = "Hard"
    
    # Human (X) takes 0 and 1. AI (O) must take 2 to block.
    app.handle_click(0) # Human
    # AI moves automatically
    app.handle_click(1) # Human
    # AI moves automatically
    
    # Check if AI blocked at index 2
    assert app.engine.board[2] == CellState.PLAYER_O or app.engine.board[2] != CellState.EMPTY

if __name__ == "__main__":
    pytest.main([__file__])