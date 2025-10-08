"""Restart services to apply theme changes"""

import subprocess
import time


def restart_services():
    """Restart qtile and dunst to apply changes"""
    try:
        # Restart qtile using correct command
        subprocess.run(["qtile", "cmd-obj", "-o", "root", "-f", "reload_config"], check=True)
        
        # Restart dunst
        subprocess.run(["pkill", "dunst"], check=False)
        # Give it a moment to close
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
