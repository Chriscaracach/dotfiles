"""UI for theme selection"""

import subprocess


def show_rofi_menu(themes):
    """Show rofi menu to select theme"""
    theme_names = list(themes.keys())
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
