"""
Current Theme Colors
Provides color variables for the active theme.
Import this module to get the current theme colors in your Qtile config.
"""

from pathlib import Path
from themes_config import ALL_THEMES

# Default theme if no current theme is set
DEFAULT_THEME = "Dark Grey"


def get_current_theme_name():
    """Get the currently active theme name from the saved state"""
    current_theme_file = Path.home() / ".config" / "qtile" / ".current_theme"
    
    if current_theme_file.exists():
        try:
            return current_theme_file.read_text().strip()
        except Exception:
            pass
    
    return DEFAULT_THEME


def load_theme_colors():
    """Load colors from the current theme"""
    theme_name = get_current_theme_name()
    
    # Find the theme in ALL_THEMES
    for theme in ALL_THEMES:
        if theme.get("name") == theme_name:
            return theme
    
    # Fallback to default theme if current theme not found
    for theme in ALL_THEMES:
        if theme.get("name") == DEFAULT_THEME:
            return theme
    
    # Last resort: use first theme
    if ALL_THEMES:
        return ALL_THEMES[0]
    
    # Emergency fallback if no themes defined
    return {
        "color_dark": "#2c2c2c",
        "color_middark": "#4a4a4a",
        "color_midlight": "#aeaeae",
        "color_light": "#d8d8d8",
        "color_lighter": "#ffffff"
    }


# Load current theme colors
_current_theme = load_theme_colors()

# Export color variables for use in Qtile config
color_dark = _current_theme["color_dark"]
color_middark = _current_theme["color_middark"]
color_midlight = _current_theme["color_midlight"]
color_light = _current_theme["color_light"]
color_lighter = _current_theme["color_lighter"]

# General colors (not theme-specific)
color_error = "#C62300"
