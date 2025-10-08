"""Update Fish shell prompt colors"""

from pathlib import Path


def update_fish_theme(theme_colors):
    """Update Fish shell prompt colors"""
    fish_config = Path.home() / ".config" / "fish" / "config.fish"
    
    if not fish_config.exists():
        return
    
    with open(fish_config, 'r') as f:
        content = f.read()
    
    # Determine if it's a light or dark theme
    is_light_theme = theme_colors["color_dark"] == "#fff"
    
    # Remove existing theme configuration if present
    lines = content.split('\n')
    new_lines = []
    skip_theme_block = False
    
    for line in lines:
        if line.strip() == "# Theme colors - managed by theme_switcher.py":
            skip_theme_block = True
            continue
        elif skip_theme_block and line.strip() == "# End theme colors":
            skip_theme_block = False
            continue
        elif not skip_theme_block:
            new_lines.append(line)
    
    # Add new theme configuration
    theme_config = "\n# Theme colors - managed by theme_switcher.py\n"
    
    if is_light_theme:
        theme_config += "set -g fish_color_normal 2c2c2c\n"
        theme_config += "set -g fish_color_command 4a4a4a\n"
        theme_config += "set -g fish_color_param 2c2c2c\n"
        theme_config += "set -g fish_color_error ff0000\n"
    else:
        accent = theme_colors["color_light"].replace("#", "")
        fg = theme_colors["color_lighter"].replace("#", "")
        theme_config += f"set -g fish_color_normal {fg}\n"
        theme_config += f"set -g fish_color_command {accent}\n"
        theme_config += f"set -g fish_color_param {fg}\n"
        theme_config += "set -g fish_color_error ff0000\n"
    
    theme_config += "# End theme colors\n"
    
    new_content = '\n'.join(new_lines).rstrip() + '\n' + theme_config
    
    with open(fish_config, 'w') as f:
        f.write(new_content)
    
    print("Fish theme updated")
