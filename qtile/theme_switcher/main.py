#!/usr/bin/env python3
"""
Theme Switcher for Qtile Configuration
Switches between different color themes and updates all config files
"""

import sys

from themes import THEMES
from qtile_colors import update_colors_py
from dunst import update_dunst_config
from rofi import update_rofi_config
from windsurf import update_windsurf_theme
from alacritty import update_alacritty_theme
from fish import update_fish_theme
from wallpaper import update_wallpaper
from services import restart_services
from ui import show_rofi_menu


def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Theme name provided as argument
        theme_name = " ".join(sys.argv[1:])
    else:
        # Show rofi menu
        theme_name = show_rofi_menu(THEMES)
    
    if not theme_name or theme_name not in THEMES:
        print("No valid theme selected or theme not found.")
        return
    
    theme_colors = THEMES[theme_name]
    
    print(f"Switching to theme: {theme_name}")
    
    # Update configuration files
    update_colors_py(theme_name, theme_colors)
    update_dunst_config(theme_colors)
    update_rofi_config(theme_colors)
    update_windsurf_theme(theme_colors)
    update_alacritty_theme(theme_colors)
    update_fish_theme(theme_colors)
    
    # Update wallpaper to match theme
    update_wallpaper()
    
    # Restart services
    restart_services()
    
    print(f"Theme switched to: {theme_name}")


if __name__ == "__main__":
    main()
