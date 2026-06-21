# Colors come from the active theme: ~/.config/themes/current/qtile.py
# Switch themes with mod+u (menus/theme.sh). The Nord values below are a
# fallback for when no theme symlink exists yet.

import os

color_dark = "#2e3440"
color_light = "#88c0d0"
color_accent = "#81a1c1"
color_fg = "#eceff4"
color_bg = "#2e3440"
color_middark = "#3b4252"
color_red = "#bf616a"
color_green = "#a3be8c"
color_yellow = "#ebcb8b"
color_blue = "#81a1c1"
color_magenta = "#b48ead"
color_cyan = "#88c0d0"

_theme = os.path.expanduser("~/.config/themes/current/qtile.py")
if os.path.exists(_theme):
    with open(_theme) as _f:
        exec(_f.read())
