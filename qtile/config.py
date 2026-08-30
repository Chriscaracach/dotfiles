# This is my qtile config. It can be used either desktop or laptop. Just check the commented lines.
#
# Version 2.0.1 - 10/7/25

# |--- TODO ---|#


# |--- IMPORTS ---|#
import os
import subprocess
import sys
from pathlib import Path

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from backend import IS_WAYLAND
from colors import *
from keys import init_keys
from layouts import init_layouts
from widgets import init_widgets_list

mod = "mod4"
terminal = guess_terminal()

# |--- GROUPS ---|#
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

# |--- KEYS ---|#
keys = init_keys(mod, terminal, groups)

# |--- LAYOUTS ---|
layouts, floating_layout = init_layouts(color_dark, color_light)

widget_defaults = dict(
    font="Hack Nerd Font Mono",
    fontsize=14,
    padding=5,
)

extension_defaults = widget_defaults.copy()

# The wallpaper picker (mod+w, menus/wallpaper.sh) flips this symlink; we
# resolve it here so the choice survives reloads and restarts. Falls back to a
# fixed image when the symlink has never been set.
_WALLPAPER_LINK = Path.home() / ".config/qtile/current-wallpaper"
WALLPAPER = (
    str(_WALLPAPER_LINK.resolve())
    if _WALLPAPER_LINK.exists()
    else str(Path.home() / "wallpapers/art-lake.png")
)

def make_screen():
    """One Screen with its own bar.

    Two Screens are defined so that dual-monitor mode gets a bar on BOTH
    outputs. With only one configured, qtile hands the second output a
    bar-less screen, which looks like the layout has come apart.
    Extra Screens are harmless when only one output is enabled.

    init_widgets_list() is called per screen on purpose: a widget instance
    cannot be shared between two bars.
    """
    return Screen(
        top=bar.Bar(
            [*init_widgets_list()],
            40,
            background=color_bg,
            margin=5,
        ),
        # Native to qtile on both backends - no nitrogen, no swaybg.
        # "fill" matches nitrogen's mode=4 (zoom-fill).
        wallpaper=WALLPAPER,
        wallpaper_mode="fill",
    )


screens = [make_screen(), make_screen()]

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
if IS_WAYLAND:
    from libqtile.backend.wayland import InputConfig

    # Applied per-device as devices appear, so hotplugged keyboards get the
    # layout too - something `setxkbmap latam` at startup never did.
    wl_input_rules = {
        "type:keyboard": InputConfig(kb_layout="latam"),
        "type:touchpad": InputConfig(tap=True, natural_scroll=True, dwt=True),
    }
else:
    wl_input_rules = None

wl_xcursor_theme = None
wl_xcursor_size = 24
wmname = "LG3D"  # X11 only; inert on Wayland

# Shared by both backends.
autostart = [
    "dunst",       # Notifications
    "nm-applet",   # Network manager tray icon (shows via widget.StatusNotifier)
]

if IS_WAYLAND:
    autostart += [
        # kanshi detects which outputs are connected and re-fires on hotplug;
        # monitors.sh applies the geometry. See scripts/monitors.sh for why the
        # two are split.
        "sh ~/.config/qtile/scripts/monitors.sh auto",
        "kanshi",
    ]
else:
    autostart += [
        "picom",                                     # Compositor
        "setxkbmap latam",                           # Keyboard layout
        "sh ~/.config/qtile/scripts/check_monitors.sh",  # HDMI detection
    ]


@hook.subscribe.startup_once
def _autostart():
    """Run once per session.

    This used to be a bare loop at module level, which meant every
    lazy.reload_config() - including the one menus/theme.sh fires on each
    theme switch - spawned another dunst/picom/nitrogen.
    """
    if IS_WAYLAND:
        # The Wayland equivalent of /etc/X11/xinit/xinitrc.d: make the session
        # environment visible to systemd --user and D-Bus-activated services
        # (portals, tray apps). WAYLAND_DISPLAY only exists once we are up, so
        # this cannot live in the launcher script.
        subprocess.run(
            [
                "dbus-update-activation-environment",
                "--systemd",
                "WAYLAND_DISPLAY",
                "DISPLAY",
                "XDG_CURRENT_DESKTOP",
                "XDG_SESSION_TYPE",
                "DESKTOP_SESSION",
            ],
            check=False,
        )

    for cmd in autostart:
        subprocess.Popen(cmd, shell=True)
