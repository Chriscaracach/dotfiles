"""Update Qtile colors.py file"""

from pathlib import Path


def get_config_dir():
    """Get the qtile config directory"""
    return Path.home() / ".config" / "qtile"


def update_colors_py(theme_name, theme_colors):
    """Update the colors.py file with the selected theme"""
    colors_file = get_config_dir() / "colors.py"
    
    # Read current file
    with open(colors_file, 'r') as f:
        lines = f.readlines()
    
    # Find and update active color definitions
    new_lines = []
    
    for line in lines:
        # Update active color definitions (not commented ones)
        if line.startswith('color_dark =') and not line.strip().startswith('#'):
            new_lines.append(f'color_dark = "{theme_colors["color_dark"]}"      # {theme_name}\n')
        elif line.startswith('color_middark =') and not line.strip().startswith('#'):
            new_lines.append(f'color_middark = "{theme_colors["color_middark"]}"   # {theme_name}\n')
        elif line.startswith('color_midlight =') and not line.strip().startswith('#'):
            new_lines.append(f'color_midlight = "{theme_colors["color_midlight"]}"  # {theme_name}\n')
        elif line.startswith('color_light =') and not line.strip().startswith('#'):
            new_lines.append(f'color_light = "{theme_colors["color_light"]}"     # {theme_name}\n')
        elif line.startswith('color_lighter =') and not line.strip().startswith('#'):
            new_lines.append(f'color_lighter = "{theme_colors["color_lighter"]}"   # {theme_name}\n')
        else:
            new_lines.append(line)
    
    # Write updated file
    with open(colors_file, 'w') as f:
        f.writelines(new_lines)
