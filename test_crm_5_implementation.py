import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from crm_5_implementation import TicTacToeApp, HOST, PORT, DEBUG, TIC_TAC_TOE_TEMPLATE

@pytest.fixture
def app_instance():
    """Fixture to provide a fresh instance of TicTacToeApp for each test."""
    return TicTacToeApp()

@pytest.fixture
def client(app_instance):
    """Fixture to provide a Flask test client."""
    app_instance.app.config['TESTING'] = True
    return app_instance.app.test_client()

def test_app_initialization(app_instance):
    """
    Test that the TicTacToeApp initializes correctly.
    Verifies that the Flask app object is created and routes are set.
    """
    assert isinstance(app_instance.app, Flask)
    assert app_instance.app.name == "crm_5_implementation"

def test_index_route_success(client):
    """
    Positive test case for the index route.
    Verifies that the root URL returns a 200 OK status and contains expected HTML content.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert "Tic Tac Toe" in response.get_data(as_text=True)
    assert "GameEngine" in response.get_data(as_text=True)
    assert "UIController" in response.get_data(as_text=True)

def test_index_route_template_error(app_instance):
    """
    Negative test case for the index route.
    Mocks render_template_string to raise an exception and verifies 500 error handling.
    """
    with patch('crm_5_implementation.render_template_string') as mocked_render:
        mocked_render.side_effect = Exception("Template rendering failed")
        
        # We need to use the app's test client
        with app_instance.app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 500
            assert b"Internal Server Error" in response.data

def test_run_method_success(app_instance):
    """
    Positive test case for the run method.
    Verifies that the Flask run method is called with the correct parameters.
    """
    with patch.object(app_instance.app, 'run') as mocked_run:
        app_instance.run(host="127.0.0.1", port=8080, debug=True)
        mocked_run.assert_called_once_with(host="127.0.0.1", port=8080, debug=True)

def test_run_method_default_parameters(app_instance):
    """
    Test the run method with default configuration constants.
    """
    with patch.object(app_instance.app, 'run') as mocked_run:
        app_instance.run()
        mocked_run.assert_called_once_with(host=HOST, port=PORT, debug=DEBUG)

def test_run_method_failure(app_instance):
    """
    Edge case: Test the run method when the server fails to start.
    Verifies that the critical error is logged.
    """
    with patch.object(app_instance.app, 'run', side_effect=RuntimeError("Port in use")):
        with patch('crm_5_implementation.logger.critical') as mocked_log:
            app_instance.run()
            mocked_log.assert_called_once()
            assert "Server failed to start" in mocked_log.call_args[0][0]

def test_constants_values():
    """
    Verify that the configuration constants are set to expected production values.
    """
    assert HOST == "0.0.0.0"
    assert PORT == 5000
    assert DEBUG is False

def test_template_content_integrity():
    """
    Verify that the HTML template contains essential UI components.
    """
    assert 'id="board"' in TIC_TAC_TOE_TEMPLATE
    assert 'id="status"' in TIC_TAC_TOE_TEMPLATE
    assert 'id="reset"' in TIC_TAC_TOE_TEMPLATE
    assert 'class="cell"' in TIC_TAC_TOE_TEMPLATE

def test_logger_configuration():
    """
    Verify that the logger is correctly named.
    """
    from crm_5_implementation import logger
    assert logger.name == "crm_5_implementation"

@pytest.mark.parametrize("path", ["/invalid", "/game", "/api"])
def test_invalid_routes(client, path):
    """
    Negative test case: Verify that undefined routes return 404.
    """
    response = client.get(path)
    assert response.status_code == 404

def test_index_route_logging(app_instance):
    """
    Test that errors during rendering are logged.
    """
    with patch('crm_5_implementation.render_template_string', side_effect=Exception("Log Test")):
        with patch('crm_5_implementation.logger.error') as mocked_error_log:
            with app_instance.app.test_client() as client:
                client.get('/')
                mocked_error_log.assert_called_once()
                assert "Error rendering template" in mocked_error_log.call_args[0][0]

def test_app_setup_routes_called(app_instance):
    """
    Verify that _setup_routes is called during initialization.
    """
    with patch.object(TicTacToeApp, '_setup_routes') as mocked_setup:
        # Re-instantiate to trigger the constructor
        TicTacToeApp()
        mocked_setup.assert_called_once()

def test_flask_app_config(app_instance):
    """
    Verify Flask internal configuration.
    """
    assert app_instance.app.static_folder is None # Default when not specified in this setup
    assert app_instance.app.template_folder == 'templates' # Flask default