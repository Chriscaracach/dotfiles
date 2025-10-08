"""Update Rofi colors"""

import re
from pathlib import Path


def update_rofi_config(theme_colors):
    """Update rofi colors"""
    rofi_file = Path.home() / ".config" / "rofi" / "config.rasi"
    
    if not rofi_file.exists():
        return
        
    with open(rofi_file, 'r') as f:
        content = f.read()
    
    # Determine colors based on theme
    is_light_theme = theme_colors["color_dark"] == "#fff"
    
    if is_light_theme:
        bg = "#fff"
        bg_alt = "#d8d8d8" 
        fg = "#2c2c2c"
        fg_alt = "#4a4a4a"
    else:
        bg = theme_colors["color_dark"]
        bg_alt = theme_colors["color_middark"]
        fg = theme_colors["color_light"] 
        fg_alt = theme_colors["color_lighter"]
    
    # Replace color definitions
    content = re.sub(r'bg: #[0-9a-fA-F]{3,6};', f'bg: {bg};', content)
    content = re.sub(r'bg-alt: #[0-9a-fA-F]{3,6};', f'bg-alt: {bg_alt};', content)
    content = re.sub(r'fg: #[0-9a-fA-F]{3,6};', f'fg: {fg};', content)
    content = re.sub(r'fg-alt: #[0-9a-fA-F]{3,6};', f'fg-alt: {fg_alt};', content)
    
    with open(rofi_file, 'w') as f:
        f.write(content)
