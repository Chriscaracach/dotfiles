"""Update Alacritty terminal colors"""

from pathlib import Path


def update_alacritty_theme(theme_colors):
    """Update Alacritty terminal colors"""
    alacritty_config = Path.home() / ".config" / "alacritty" / "alacritty.toml"
    
    if not alacritty_config.exists():
        return
    
    with open(alacritty_config, 'r') as f:
        lines = f.readlines()
    
    # Determine if it's a light or dark theme
    is_light_theme = theme_colors["color_dark"] == "#fff"
    
    if is_light_theme:
        # Light theme colors
        bg = "0xffffff"
        fg = "0x2c2c2c"
        cursor = "0x4a4a4a"
        accent = theme_colors["color_light"].replace("#", "0x")
    else:
        # Dark theme colors
        bg = theme_colors["color_dark"].replace("#", "0x")
        fg = theme_colors["color_lighter"].replace("#", "0x")
        cursor = theme_colors["color_light"].replace("#", "0x")
        accent = theme_colors["color_midlight"].replace("#", "0x")
    
    new_lines = []
    for line in lines:
        if line.strip().startswith("background ="):
            new_lines.append(f'background = "{bg}"\n')
        elif line.strip().startswith("foreground ="):
            new_lines.append(f'foreground = "{fg}"\n')
        elif line.strip().startswith("cyan ="):
            new_lines.append(f'cyan = "{accent}"\n')
        else:
            new_lines.append(line)
    
    with open(alacritty_config, 'w') as f:
        f.writelines(new_lines)
    
    print("Alacritty theme updated")
