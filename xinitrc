#!/bin/sh
# Started via `startx` from a TTY login. Launches qtile (X11).

# Session identity — set before the xinitrc.d hooks so they propagate it
export XDG_SESSION_DESKTOP=qtile
export XDG_CURRENT_DESKTOP=qtile
export DESKTOP_SESSION=qtile

# System hooks: imports DISPLAY/XAUTHORITY into systemd --user and D-Bus,
# sets GTK modules, etc.
if [ -d /etc/X11/xinit/xinitrc.d ]; then
    for f in /etc/X11/xinit/xinitrc.d/?*.sh; do
        [ -x "$f" ] && . "$f"
    done
    unset f
fi

# Make XDG_CURRENT_DESKTOP visible to D-Bus-activated apps (portals, etc.)
if command -v dbus-update-activation-environment >/dev/null 2>&1; then
    dbus-update-activation-environment --systemd XDG_CURRENT_DESKTOP DESKTOP_SESSION 2>/dev/null
fi

xrandr --auto
exec qtile start
