import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from crm_5_implementation import TicTacToeApp

@pytest.fixture
def app_instance():
    """Fixture to provide a TicTacToeApp instance for testing."""
    return TicTacToeApp(host='127.0.0.1', port=8080, debug=False)

@pytest.fixture
def client(app_instance):
    """Fixture to provide a Flask test client."""
    app_instance.app.config['TESTING'] = True
    with app_instance.app.test_client() as client:
        yield client

def test_initialization(app_instance):
    """
    Test that the TicTacToeApp initializes with correct attributes.
    """
    assert app_instance.host == '127.0.0.1'
    assert app_instance.port == 8080
    assert app_instance.debug is False
    assert isinstance(app_instance.app, Flask)

def test_index_route_success(client):
    """
    Test the index route ('/') to ensure it returns 200 OK and contains expected HTML content.
    """
    response = client.get('/')
    assert response.status_code == 200
    html_content = response.data.decode('utf-8')
    assert '<title>CRM-5: Tic Tac Toe</title>' in html_content
    assert 'id="board"' in html_content
    assert 'class="cell"' in html_content
    assert 'id="reset-btn"' in html_content
    assert 'const TicTacToe =' in html_content

def test_index_route_template_rendering_failure(app_instance):
    """
    Test the index route error handling when template rendering fails.
    """
    with patch('crm_5_implementation.render_template_string') as mocked_render:
        mocked_render.side_effect = Exception("Template Error")
        
        with app_instance.app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 500
            assert b"Internal Server Error" in response.data

def test_run_method_success(app_instance):
    """
    Test the run method to ensure it calls Flask's run with correct arguments.
    """
    with patch.object(app_instance.app, 'run') as mocked_run:
        app_instance.run()
        mocked_run.assert_called_once_with(
            host='127.0.0.1', 
            port=8080, 
            debug=False
        )

def test_run_method_exception(app_instance):
    """
    Test the run method's exception handling when Flask fails to start.
    """
    with patch.object(app_instance.app, 'run') as mocked_run:
        mocked_run.side_effect = Exception("Port already in use")
        with patch('crm_5_implementation.logger.critical') as mocked_logger:
            app_instance.run()
            mocked_logger.assert_called_once()
            assert "Failed to start server" in mocked_logger.call_args[0][0]

def test_template_content_integrity(app_instance):
    """
    Test that the TEMPLATE constant contains essential game logic and styles.
    """
    template = app_instance.TEMPLATE
    # Check CSS variables
    assert '--x-color' in template
    assert '--o-color' in template
    # Check Grid layout
    assert 'display: grid' in template
    # Check JS Logic
    assert 'winningConditions' in template
    assert 'handleCellClick' in template
    assert 'restartGame' in template
    # Check Event Listeners
    assert "addEventListener('click', TicTacToe.handleCellClick)" in template

def test_custom_config_initialization():
    """
    Test initialization with non-default host and port.
    """
    custom_app = TicTacToeApp(host='192.168.1.1', port=9000, debug=True)
    assert custom_app.host == '192.168.1.1'
    assert custom_app.port == 9000
    assert custom_app.debug is True

def test_index_route_contains_all_cells(client):
    """
    Verify that the rendered HTML contains all 9 cells for the Tic Tac Toe board.
    """
    response = client.get('/')
    html_content = response.data.decode('utf-8')
    for i in range(9):
        assert f'data-index="{i}"' in html_content

@pytest.mark.parametrize("element", [
    "status-indicator",
    "game-board",
    "cell",
    "controls",
    "reset-btn"
])
def test_ui_elements_presence(client, element):
    """
    Verify the presence of essential UI class names and IDs in the response.
    """
    response = client.get('/')
    assert element.encode() in response.data

def test_logger_info_on_run(app_instance):
    """
    Verify that the server logs an info message when starting.
    """
    with patch.object(app_instance.app, 'run'):
        with patch('crm_5_implementation.logger.info') as mocked_info:
            app_instance.run()
            mocked_info.assert_called()
            assert "Starting Tic Tac Toe server" in mocked_info.call_args[0][0]

def test_route_registration(app_instance):
    """
    Verify that the '/' route is correctly registered in the Flask app.
    """
    rules = [rule.rule for rule in app_instance.app.url_map.iter_rules()]
    assert '/' in rules

def test_template_is_final_string(app_instance):
    """
    Ensure the TEMPLATE is a string and not empty.
    """
    assert isinstance(app_instance.TEMPLATE, str)
    assert len(app_instance.TEMPLATE) > 0

def test_internal_server_error_logging(app_instance):
    """
    Verify that template rendering errors are logged as errors.
    """
    with patch('crm_5_implementation.render_template_string', side_effect=Exception("Render fail")):
        with patch('crm_5_implementation.logger.error') as mocked_error:
            with app_instance.app.test_client() as client:
                client.get('/')
                mocked_error.assert_called_once()
                assert "Error rendering template" in mocked_error.call_args[0][0]