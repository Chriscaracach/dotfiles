"""
Theme Configuration File
=========================

This file contains all theme definitions for the Qtile theme switcher.
Each theme must have the following 5 color values:
- color_dark: Darkest shade
- color_middark: Medium dark shade
- color_midlight: Medium light shade
- color_light: Light shade
- color_lighter: Lightest shade

To add a new theme:
1. Copy one of the theme blocks below
2. Uncomment it (remove the # at the start of each line)
3. Change the theme name and colors
4. The theme will automatically appear in the theme switcher

To activate a theme:
- Uncomment the theme block you want to use
- Make sure only one theme is active at a time (all others should be commented out)
"""

# =============================================================================
# WORK THEMES
# =============================================================================

# Work Theme - Cyan
# Palette based on cyan (#0DCDCD)
WORK_CYAN = {
    "name": "Work (Cyan)",
    "color_dark": "#085e5e",      # much darker
    "color_middark": "#099e9e",   # slightly darker
    "color_midlight": "#0ba5a5",  # a little darker than light
    "color_light": "#0DCDCD",     # base
    "color_lighter": "#b6fafa"    # much lighter
}

# Work Theme - Blue Ocean
WORK_BLUE = {
    "name": "Blue Ocean",
    "color_dark": "#04364A",
    "color_middark": "#176B87",
    "color_midlight": "#64CCC5",
    "color_light": "#DAFFFB",
    "color_lighter": "#FFFFFF"
}

# =============================================================================
# PERSONAL THEMES
# =============================================================================

# Personal Theme - Purple
PERSONAL_PURPLE = {
    "name": "Purple",
    "color_dark": "#2E073F",
    "color_middark": "#7A1CAC",
    "color_midlight": "#AD49E1",
    "color_light": "#E49BFF",
    "color_lighter": "#EBD3F8"
}

# =============================================================================
# NEUTRAL THEMES
# =============================================================================

# Dark Grey Theme
DARK_GREY = {
    "name": "Dark Grey",
    "color_dark": "#2c2c2c",      # dark grey
    "color_middark": "#4a4a4a",   # medium dark grey
    "color_midlight": "#aeaeae",  # medium light grey
    "color_light": "#d8d8d8",     # light grey
    "color_lighter": "#fff"       # white
}

# Light Grey Theme (inverted colors for light mode)
LIGHT_GREY = {
    "name": "Light Grey",
    "color_dark": "#fff",         # white
    "color_middark": "#d8d8d8",   # light grey
    "color_midlight": "#aeaeae",  # medium light grey
    "color_light": "#4a4a4a",     # medium dark grey
    "color_lighter": "#2c2c2c"    # dark grey
}

# =============================================================================
# ADD YOUR CUSTOM THEMES BELOW
# =============================================================================

# Example: Custom Theme Template (uncomment and modify to use)
MY_CUSTOM_THEME = {
    "name": "My Custom Theme",
    "color_dark": "#000000",
    "color_middark": "#333333",
    "color_midlight": "#666666",
    "color_light": "#999999",
    "color_lighter": "#CCCCCC"
}

# =============================================================================
# THEME REGISTRY
# =============================================================================
# Add all your active themes to this list
# Only themes in this list will appear in the theme switcher

ALL_THEMES = [
    WORK_CYAN,
    WORK_BLUE,
    PERSONAL_PURPLE,
    DARK_GREY,
    LIGHT_GREY,
    # Add your custom themes here:
    MY_CUSTOM_THEME,
]
