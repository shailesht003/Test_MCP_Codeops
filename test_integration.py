import pytest
import logging
from crm_5_implementation import app, HOST, PORT, DEBUG

@pytest.fixture
def client():
    """
    Fixture to initialize the Flask test client.
    Sets the application to testing mode and yields the client for integration requests.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_server_configuration_integrity():
    """
    Integration test to verify that the server configuration constants 
    defined in the implementation file are correctly assigned.
    """
    assert HOST == "0.0.0.0"
    assert PORT == 5000
    assert DEBUG is False

def test_index_route_accessibility(client):
    """
    Integration test for the root endpoint. 
    Ensures the Flask server is running and the index route returns a 200 OK status.
    """
    response = client.get('/')
    assert response.status_code == 200

def test_template_rendering_integration(client):
    """
    Integration test to verify the connection between the Flask route and the 
    TIC_TAC_TOE_TEMPLATE. Checks if the HTML, CSS, and JS components are served.
    """
    response = client.get('/')
    content = response.data.decode('utf-8')
    
    # Verify the page contains the game title
    assert "Tic Tac Toe" in content
    
    # Verify the integration of CSS styles
    assert "<style>" in content
    
    # Verify the integration of the JavaScript Game Logic Engine
    assert "<script>" in content
    
    # Verify the existence of the game board container in the rendered HTML
    assert "board" in content.lower()

def test_content_type_header(client):
    """
    Integration test to ensure the server correctly identifies the 
    response as HTML.
    """
    response = client.get('/')
    assert "text/html" in response.headers['Content-Type']

def test_logging_system_initialization():
    """
    Integration test to verify that the logging configuration is 
    properly initialized for production monitoring.
    """
    logger = logging.getLogger("crm_5_implementation")
    assert logger is not None
    # Verify root or module logger has a level set (defaulting to INFO in implementation)
    assert logging.getLogger().getEffectiveLevel() <= logging.INFO

def test_error_handling_integration(client):
    """
    Integration test to verify that the application correctly handles 
    requests to non-existent endpoints.
    """
    response = client.get('/invalid-game-route')
    assert response.status_code == 404

def test_app_instance_configuration():
    """
    Verifies that the Flask app instance is correctly named and integrated.
    """
    assert app.name == "crm_5_implementation" or app.name == "flask" or app.name == "__main__"
    assert not app.debug  # Matches DEBUG: Final[bool] = False