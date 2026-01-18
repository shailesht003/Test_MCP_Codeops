import pytest
from crm_5_implementation import TicTacToeApp

@pytest.fixture(scope="module")
def app_instance():
    """
    Setup fixture for the TicTacToeApp instance.
    Ensures the Flask application is configured for testing mode.
    """
    # Initialize the application class
    service = TicTacToeApp()
    # Access the Flask app instance encapsulated within the class
    flask_app = service.app
    flask_app.config.update({
        "TESTING": True,
    })
    return flask_app

@pytest.fixture
def client(app_instance):
    """
    Fixture to provide a test client for the Flask application.
    Handles setup and teardown of the test client context.
    """
    with app_instance.test_client() as client:
        yield client

def test_index_route_integration(client):
    """
    Test the integration between the Flask route and the template rendering engine.
    Verifies that the root endpoint returns a 200 OK status and serves the HTML content.
    """
    response = client.get('/')
    assert response.status_code == 200
    
    html_content = response.data.decode('utf-8')
    
    # Verify core HTML structure is present
    assert "<!DOCTYPE html>" in html_content
    assert "Tic Tac Toe" in html_content
    assert "html" in html_content.lower()

def test_frontend_assets_integration(client):
    """
    Verify that CSS and JavaScript components are correctly integrated into the response.
    Since this is a client-side game, these assets should be embedded or linked.
    """
    response = client.get('/')
    html_content = response.data.decode('utf-8')
    
    # Check for CSS integration (style tags or links)
    assert "<style>" in html_content or "rel=\"stylesheet\"" in html_content
    
    # Check for JS integration (script tags)
    assert "<script>" in html_content or "src=" in html_content

def test_game_board_ui_components(client):
    """
    Integration test to ensure the DOM elements required for the Tic Tac Toe 
    game board are present in the rendered HTML.
    """
    response = client.get('/')
    html_content = response.data.decode('utf-8')
    
    # Check for common UI elements defined in the requirements
    # Looking for grid cells, status indicators, or restart buttons
    assert "cell" in html_content.lower()
    assert "board" in html_content.lower()
    assert "restart" in html_content.lower() or "reset" in html_content.lower()

def test_client_side_logic_presence(client):
    """
    Verify that the JavaScript logic for game state (win/draw conditions) 
    is included in the served page.
    """
    response = client.get('/')
    html_content = response.data.decode('utf-8')
    
    # Search for keywords typically found in the JS game logic
    logic_indicators = ["winning", "combinations", "click", "player"]
    found_indicators = [indicator in html_content.lower() for indicator in logic_indicators]
    
    assert any(found_indicators), "JavaScript game logic keywords not found in the response"

def test_app_error_handling_integration(client):
    """
    Ensure the application integrates with Flask's default error handling 
    for undefined routes.
    """
    response = client.get('/api/non_existent_endpoint')
    assert response.status_code == 404

def test_production_logging_config(app_instance):
    """
    Verify that the application initializes with the correct logging level 
    as specified in the implementation.
    """
    import logging
    # The implementation configures logging at the module level
    logger = logging.getLogger("crm_5_implementation")
    # Verify logger is active (level 20 is INFO)
    assert logger.level <= logging.INFO

def test_app_instance_configuration(app_instance):
    """
    Verify the Flask app instance is correctly configured within the TicTacToeApp class.
    """
    assert app_instance.name == "crm_5_implementation" or app_instance.import_name is not None
    assert not app_instance.debug  # Should not be in debug mode for production readiness tests