"""Update Windsurf (VSCode) theme"""

import json
from pathlib import Path


def update_windsurf_theme(theme_colors):
    """Update Windsurf (VSCode) theme"""
    windsurf_settings = Path.home() / ".config" / "Windsurf" / "User" / "settings.json"
    
    if not windsurf_settings.exists():
        return
    
    # Determine if it's a light or dark theme
    is_light_theme = theme_colors["color_dark"] == "#fff"
    
    # Set appropriate GitHub theme
    if is_light_theme:
        theme_name = "GitHub Light High Contrast"
    else:
        theme_name = "GitHub Dark High Contrast"
    
    try:
        with open(windsurf_settings, 'r') as f:
            settings = json.load(f)
        
        settings["workbench.colorTheme"] = theme_name
        
        with open(windsurf_settings, 'w') as f:
            json.dump(settings, f, indent=2)
        
        print(f"Windsurf theme set to: {theme_name}")
    except Exception as e:
        print(f"Error updating Windsurf theme: {e}")
