import pytest
import json
from typing import Dict
from your_module import ConfigManager  # Replace with actual module name

@pytest.fixture
def temp_config_file(tmp_path):
    """Fixture to create a temporary config file with grey theme."""
    config_data = {
        "theme": "grey",
        "bg_color": "#cccccc",
        "fg_color": "#333333",
        "highlight_color": "#999999"
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config_data))
    return config_path

def test_singleton_pattern(temp_config_file):
    """Test that ConfigManager is a singleton."""
    cm1 = ConfigManager()
    cm2 = ConfigManager()
    assert cm1 is cm2, "ConfigManager should be a singleton instance"

def test_default_theme(temp_config_file):
    """Test that ConfigManager defaults to grey theme."""
    cm = ConfigManager()
    assert cm.theme == "grey", "Default theme should be grey"

def test_config_loading(temp_config_file):
    """Test that ConfigManager loads configuration from the file."""
    cm = ConfigManager()
    assert cm.theme == "grey", "Theme should be grey"
    assert cm.bg_color == "#cccccc", "Background color should match"
    assert cm.fg_color == "#333333", "Foreground color should match"
    assert cm.highlight_color == "#999999", "Highlight color should match"

def test_config_overwrite(temp_config_file):
    """Test that ConfigManager can be initialized with a custom config file."""
    cm = ConfigManager(config_path=temp_config_file)
    assert cm.theme == "grey", "Theme should be grey"
    assert cm.bg_color == "#cccccc", "Background color should match"
    assert cm.fg_color == "#333333", "Foreground color should match"
    assert cm.highlight_color == "#999999", "Highlight color should match"