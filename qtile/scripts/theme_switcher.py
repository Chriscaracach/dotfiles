#!/usr/bin/env python3
"""
Theme Switcher for Qtile Configuration
Wrapper script that calls the modular theme switcher
"""

import sys
from pathlib import Path

# Add theme_switcher package to path
theme_switcher_path = Path.home() / ".config" / "qtile" / "theme_switcher"
sys.path.insert(0, str(theme_switcher_path))

from main import main

if __name__ == "__main__":
    main()

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
    import re
    content = re.sub(r'bg: #[0-9a-fA-F]{3,6};', f'bg: {bg};', content)
    content = re.sub(r'bg-alt: #[0-9a-fA-F]{3,6};', f'bg-alt: {bg_alt};', content)
    content = re.sub(r'fg: #[0-9a-fA-F]{3,6};', f'fg: {fg};', content)
    content = re.sub(r'fg-alt: #[0-9a-fA-F]{3,6};', f'fg-alt: {fg_alt};', content)
    
    with open(rofi_file, 'w') as f:
        f.write(content)

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

def update_wallpaper():
    """Update wallpaper based on theme"""
    wallpaper_script = get_config_dir() / "scripts" / "set_random_wallpaper.sh"
    
    if wallpaper_script.exists():
        try:
            subprocess.run([str(wallpaper_script)], check=True)
            print("Wallpaper updated")
        except subprocess.CalledProcessError as e:
            print(f"Error updating wallpaper: {e}")
    else:
        print(f"Wallpaper script not found: {wallpaper_script}")

def restart_services():
    """Restart qtile and dunst to apply changes"""
    try:
        # Restart qtile using correct command
        subprocess.run(["qtile", "cmd-obj", "-o", "root", "-f", "reload_config"], check=True)
        
        # Restart dunst
        subprocess.run(["pkill", "dunst"], check=False)
        # Give it a moment to close
        import time
        time.sleep(0.5)
        subprocess.Popen(["dunst"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("Services restarted successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error restarting qtile: {e}")
        # Try alternative qtile restart method
        try:
            subprocess.run(["qtile", "cmd-obj", "-o", "root", "-f", "restart"], check=True)
            print("Qtile restarted instead of reloaded")
        except subprocess.CalledProcessError:
            print("Qtile restart also failed")

def show_rofi_menu():
    """Show rofi menu to select theme"""
    theme_names = list(THEMES.keys())
    rofi_input = "\n".join(theme_names)
    
    try:
        result = subprocess.run(
            ["rofi", "-dmenu", "-i", "-p", "Select Theme:", "-theme-str", 
             "window { width: 400px; } listview { lines: 5; }"],
            input=rofi_input,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Theme name provided as argument
        theme_name = " ".join(sys.argv[1:])
    else:
        # Show rofi menu
        theme_name = show_rofi_menu()
    
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
