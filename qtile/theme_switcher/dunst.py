"""Update Dunst notification colors"""

from pathlib import Path


def update_dunst_config(theme_colors):
    """Update dunst notification colors"""
    dunst_file = Path.home() / ".config" / "dunst" / "dunstrc"
    
    if not dunst_file.exists():
        return
        
    with open(dunst_file, 'r') as f:
        lines = f.readlines()
    
    # Determine if it's a light or dark theme
    is_light_theme = theme_colors["color_dark"] == "#fff"
    
    if is_light_theme:
        # Light theme colors
        bg_color = "#fff"
        fg_low = "#4a4a4a" 
        fg_normal = "#2c2c2c"
        frame_color = "#aeaeae"
    else:
        # Dark theme colors
        bg_color = theme_colors["color_dark"]
        fg_low = theme_colors["color_lighter"]
        fg_normal = theme_colors["color_lighter"] 
        frame_color = theme_colors["color_light"]
    
    # Update lines
    new_lines = []
    in_urgency_low = False
    in_urgency_normal = False
    
    for line in lines:
        if line.strip() == "[urgency_low]":
            in_urgency_low = True
            in_urgency_normal = False
            new_lines.append(line)
        elif line.strip() == "[urgency_normal]":
            in_urgency_low = False
            in_urgency_normal = True
            new_lines.append(line)
        elif line.strip().startswith("[") and line.strip() != "[urgency_low]" and line.strip() != "[urgency_normal]":
            in_urgency_low = False
            in_urgency_normal = False
            new_lines.append(line)
        elif in_urgency_low and line.strip().startswith("background ="):
            new_lines.append(f'    background = "{bg_color}"\n')
        elif in_urgency_low and line.strip().startswith("foreground ="):
            new_lines.append(f'    foreground = "{fg_low}"\n')
        elif in_urgency_low and line.strip().startswith("frame_color ="):
            new_lines.append(f'    frame_color = "{frame_color}"\n')
        elif in_urgency_normal and line.strip().startswith("background ="):
            new_lines.append(f'    background = "{bg_color}"\n')
        elif in_urgency_normal and line.strip().startswith("foreground ="):
            new_lines.append(f'    foreground = "{fg_normal}"\n')
        elif in_urgency_normal and line.strip().startswith("frame_color ="):
            new_lines.append(f'    frame_color = "{frame_color}"\n')
        else:
            new_lines.append(line)
    
    with open(dunst_file, 'w') as f:
        f.writelines(new_lines)
