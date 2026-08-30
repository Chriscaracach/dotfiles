#!/bin/bash
# Pick a random wallpaper and hand it to qtile itself. Works on both backends
# (was `nitrogen --set-zoom-fill`, which is X11-only).

WALLPAPER_DIR="$HOME/wallpapers"

RANDOM_WALLPAPER=$(find "$WALLPAPER_DIR" -type f | shuf -n 1)

if [ -f "$RANDOM_WALLPAPER" ]; then
    qtile cmd-obj -o screen -f set_wallpaper -a "$RANDOM_WALLPAPER" fill
else
    echo "No wallpaper found in $WALLPAPER_DIR"
fi
