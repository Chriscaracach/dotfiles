#!/bin/bash

WALLPAPER_DIR="$HOME/wallpapers"
COLORS_FILE="$HOME/.config/qtile/colors.py"

# Check if we're using a light or dark theme
if grep -q '^color_dark = "#fff"' "$COLORS_FILE"; then
    # Light theme - use arch3.png or arch4.png
    WALLPAPERS=("$WALLPAPER_DIR/arch3.png" "$WALLPAPER_DIR/arch4.png")
else
    # Dark theme - use arch1.png or arch2.png
    WALLPAPERS=("$WALLPAPER_DIR/arch1.png" "$WALLPAPER_DIR/arch2.png")
fi

# Select random wallpaper from the appropriate set
RANDOM_INDEX=$((RANDOM % ${#WALLPAPERS[@]}))
RANDOM_WALLPAPER="${WALLPAPERS[$RANDOM_INDEX]}"

if [ -f "$RANDOM_WALLPAPER" ]; then
    nitrogen --set-zoom-fill "$RANDOM_WALLPAPER"
else
    echo "Wallpaper not found: $RANDOM_WALLPAPER"
fi