import pytest
from unittest.mock import MagicMock, patch
from crm_8_implementation import ColorTheme, TicTacToeBoard, TicTacToeGame, DisplayEngine

class TestTicTacToeGreenThemeIntegration:
    """
    Integration tests for the Tic Tac Toe CRM-8 Green Color Update.
    Verifies interaction between ColorTheme, Board logic, and Display output.
    """

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """
        Setup and teardown for each test case.
        Ensures a clean state for the ColorTheme configuration.
        """
        # Setup logic if global state existed
        yield
        # Teardown logic if global state existed

    @pytest.fixture
    def game_engine(self):
        """Provides a fresh instance of the TicTacToeGame with the Green theme."""
        return TicTacToeGame(theme=ColorTheme())

    @pytest.fixture
    def mock_display(self):
        """Mocks the terminal display to capture ANSI output."""
        with patch('crm_8_implementation.DisplayEngine.render') as mocked_render:
            yield mocked_render

    def test_color_theme_integration_with_board_state(self, game_engine):
        """
        Scenario: Verify that the Board correctly associates moves with Theme colors.
        Tests integration between ColorTheme and TicTacToeBoard.
        """
        game_engine.make_move(0, 0)  # X moves to top-left
        cell_value = game_engine.board.get_cell(0, 0)
        
        # Verify the cell contains the X marker
        assert "X" in cell_value
        # Verify the cell contains the Green ANSI code defined in ColorTheme
        assert ColorTheme.X_COLOR in cell_value
        assert ColorTheme.RESET in cell_value

    def test_full_game_flow_to_victory_with_colors(self, game_engine):
        """
        Scenario: Execute a full game resulting in a win.
        Verifies that win detection logic works alongside color-coded markers.
        """
        # Moves to make X win on the top row
        moves = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)]
        for r, c in moves:
            game_engine.make_move(r, c)

        assert game_engine.check_winner() == "X"
        assert game_engine.is_game_over() is True
        
        # Verify board state integrity with colors
        board_snapshot = game_engine.board.get_grid()
        assert ColorTheme.X_COLOR in board_snapshot[0][0]
        assert ColorTheme.X_COLOR in board_snapshot[0][1]
        assert ColorTheme.X_COLOR in board_snapshot[0][2]

    def test_display_engine_renders_green_theme(self, game_engine, mock_display):
        """
        Scenario: Test the API/Interface between Game Logic and Display Engine.
        Ensures the UI component receives strings formatted with the Green theme.
        """
        game_engine.make_move(1, 1) # X takes center
        game_engine.render_board()

        # Capture the call arguments to the display engine
        args, _ = mock_display.call_args
        rendered_output = args[0]

        assert ColorTheme.X_COLOR in rendered_output
        assert "X" in rendered_output
        assert ColorTheme.PRIMARY_COLOR == "Green"

    def test_theme_contrast_between_players(self, game_engine):
        """
        Scenario: Verify that X (Green) and O (Blue) have distinct ANSI codes in the board.
        Tests integration of multiple theme properties within the board container.
        """
        game_engine.make_move(0, 0) # X (Green)
        game_engine.make_move(1, 1) # O (Blue)

        x_cell = game_engine.board.get_cell(0, 0)
        o_cell = game_engine.board.get_cell(1, 1)

        assert ColorTheme.X_COLOR in x_cell
        assert ColorTheme.O_COLOR in o_cell
        assert x_cell != o_cell

    def test_invalid_move_does_not_affect_theme_consistency(self, game_engine):
        """
        Scenario: Attempt an invalid move and ensure the board theme remains consistent.
        """
        game_engine.make_move(0, 0)
        initial_color_count = str(game_engine.board.get_grid()).count(ColorTheme.X_COLOR)
        
        # Attempt to move in the same spot
        with pytest.raises(ValueError):
            game_engine.make_move(0, 0)
            
        final_color_count = str(game_engine.board.get_grid()).count(ColorTheme.X_COLOR)
        assert initial_color_count == final_color_count

    def test_reset_functionality_clears_colors(self, game_engine):
        """
        Scenario: Resetting the game should clear all colored markers from the board.
        """
        game_engine.make_move(0, 0)
        game_engine.reset_game()
        
        grid = game_engine.board.get_grid()
        for row in grid:
            for cell in row:
                assert ColorTheme.X_COLOR not in cell
                assert ColorTheme.O_COLOR not in cell
                assert cell == "" or cell == " "

    @pytest.mark.parametrize("marker, expected_color", [
        ("X", ColorTheme.X_COLOR),
        ("O", ColorTheme.O_COLOR)
    ])
    def test_marker_color_mapping(self, game_engine, marker, expected_color):
        """
        Scenario: Data-driven test to ensure correct mapping of markers to theme colors.
        """
        formatted_marker = game_engine.theme.apply_color(marker)
        assert expected_color in formatted_marker
        assert marker in formatted_marker
        assert ColorTheme.RESET in formatted_marker

def test_singleton_theme_behavior():
    """
    Scenario: Ensure that the Green color update is applied globally if 
    ColorTheme is used as a configuration manager.
    """
    theme1 = ColorTheme()
    theme2 = ColorTheme()
    assert theme1.PRIMARY_COLOR == theme2.PRIMARY_COLOR
    assert theme1.PRIMARY_COLOR == "Green"