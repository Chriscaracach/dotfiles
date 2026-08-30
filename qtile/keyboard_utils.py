"""Utilities for handling keyboard layout switching.

X11 shells out to setxkbmap. Wayland has no such tool — the compositor owns
the keymap — so we drive qtile's own core.set_keymap() and track the active
layout in-process, since there is nothing to query it back from.
"""

import os
import subprocess
import time

from libqtile import qtile

from backend import IS_WAYLAND

# The layout qtile starts with. On Wayland this is set declaratively by
# wl_input_rules in config.py; on X11 by setxkbmap in the autostart hook.
_LAYOUTS = ("latam", "us")
_current = "latam"


def _label(layout):
    return "EN" if layout == "us" else "ES"


def get_layout():
    if IS_WAYLAND:
        return _label(_current)

    layout = (
        os.popen("setxkbmap -query | grep layout | awk '{print $2}'").read().strip()
    )
    return "EN" if layout == "us" else "ES"


def toggle_layout(qtile_obj=None):
    global _current

    new_layout = "us" if get_layout() == "ES" else "latam"

    if IS_WAYLAND:
        qtile.core.set_keymap(layout=new_layout)
        _current = new_layout
    else:
        os.system(f"setxkbmap {new_layout}")
        time.sleep(0.1)

    # Push the new label to every bar's indicator. This used to read
    # `from config import keyboard_widget`, which raised ImportError - the
    # widget lives in widgets.py, not config.py - so the label never updated.
    from widgets import keyboard_widgets

    for w in keyboard_widgets:
        w.update(_label(new_layout))
