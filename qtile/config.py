# This is my qtile config. It can be used either desktop or laptop. Just check the commented lines.
#
# Version 2.0.1 - 10/7/25

#|--- TODO ---|#


#|--- IMPORTS ---|#
import os
import subprocess

from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from colors import *
from keys import init_keys
from layouts import init_layouts
from widgets import init_widgets_list

mod = "mod4"
terminal = guess_terminal()

#|--- GROUPS ---|#
groups = [
    Group("1", label="\ue69d"),
    Group("2", label="\uf269"),
    Group("3", label="\ueb32"),
    Group("4", label="\ue743"),
    Group("5", label="\uf0c0"),
    Group("6", label="\uf1c0"),
    Group("7", label="\uea85"),
    Group("8", label="\ue8a4"),
    Group("9", label="\uf1ff"),
]

#|--- KEYS ---|#
keys = init_keys(mod, terminal, groups)

#|--- LAYOUTS ---|
layouts, floating_layout = init_layouts(color_dark, color_light)

widget_defaults = dict(
    font="Hack Nerd Font Mono",
    fontsize=14,
    padding=4,
)

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                *init_widgets_list()
            ],
            30,
            background=color_dark,
            border_width=[2, 2, 2, 2],
            border_color=[color_middark, color_middark, color_middark, color_middark]  
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24
wmname = "LG3D"

autostart = [
    "dunst &", # Notifications
    "picom &", # Compositor
    "nm-applet &", # Network manager
    "setxkbmap latam &", # Set keyboard layout to latam
    "sh ~/.config/qtile/scripts/check_monitors.sh", # This checks the HDMI screen, comment if you're not using it
    "sh ~/.config/qtile/scripts/set_random_wallpaper.sh" # This sets a random wallpaper based on theme
]

for cmd in autostart:
    subprocess.Popen(cmd, shell=True)
