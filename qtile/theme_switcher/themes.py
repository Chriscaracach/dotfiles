"""
Theme definitions loader
Loads themes from themes_config.py
"""

from themes_config import ALL_THEMES


def load_themes():
    """
    Load themes from themes_config.py and convert to the format expected by the theme switcher.
    Returns a dictionary with theme names as keys and color dictionaries as values.
    """
    themes = {}
    for theme in ALL_THEMES:
        theme_copy = theme.copy()
        theme_name = theme_copy.pop("name")
        themes[theme_name] = theme_copy
    return themes


# Load all themes from config
THEMES = load_themes()
