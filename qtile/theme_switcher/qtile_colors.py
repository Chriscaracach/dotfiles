"""Update Qtile theme selection"""

from pathlib import Path


def get_config_dir():
    """Get the qtile config directory"""
    return Path.home() / ".config" / "qtile"


def update_colors_py(theme_name, theme_colors):
    """
    Save the current theme selection.
    
    The colors.py file now dynamically loads from themes_config.py,
    so we just need to save which theme is active.
    """
    current_theme_file = get_config_dir() / ".current_theme"
    
    # Save the current theme name
    current_theme_file.write_text(theme_name)
