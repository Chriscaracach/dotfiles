"""Utilities for handling keyboard layout switching."""
import os
import subprocess
import time

def get_layout():
    layout = os.popen("setxkbmap -query | grep layout | awk '{print $2}'").read().strip()
    return "EN" if layout == "us" else "ES"
    
#def get_layout():
#    result = subprocess.run(
#        ["setxkbmap", "-query"],
#        capture_output=True,
#        text=True
#    )
#    for line in result.stdout.splitlines():
#        if "layout:" in line:
#            layout = line.split(":")[1].strip()
#            return "EN" if layout == "us" else "ES"
#    return "ES"

def toggle_layout(qtile):
    new_layout = "us" if get_layout() == "ES" else "latam"
    os.system(f"setxkbmap {new_layout}")
    time.sleep(0.1)

    from config import keyboard_widget
    if keyboard_widget:
        keyboard_widget.update(f"{'EN' if new_layout == 'us' else 'ES'}")
