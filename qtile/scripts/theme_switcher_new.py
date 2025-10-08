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
