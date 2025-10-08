"""Update wallpaper based on theme"""

import subprocess
from pathlib import Path


def update_wallpaper():
    """Update wallpaper based on theme"""
    wallpaper_script = Path.home() / ".config" / "qtile" / "scripts" / "set_random_wallpaper.sh"
    
    if wallpaper_script.exists():
        try:
            subprocess.run([str(wallpaper_script)], check=True)
            print("Wallpaper updated")
        except subprocess.CalledProcessError as e:
            print(f"Error updating wallpaper: {e}")
    else:
        print(f"Wallpaper script not found: {wallpaper_script}")
