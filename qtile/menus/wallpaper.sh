#!/bin/bash
# Wallpaper picker. Drop images into ~/wallpapers/ and they show up here.
#
# The choice persists via a symlink (~/.config/qtile/current-wallpaper), which
# config.py resolves at load - same idea as the theme switcher's `current`
# symlink. Runtime-only `set_wallpaper` calls would be lost on the next reload.

# rofi's Wayland backend segfaults under qtile 0.37 (mmap of size 0 -> crash in
# its own g_log path). Run it via XWayland. Scoped to the rofi call ONLY:
# unsetting WAYLAND_DISPLAY for the whole script breaks `qtile cmd-obj`, whose
# IPC socket name derives from it (libqtile/ipc.py:38).
rofi() { env -u WAYLAND_DISPLAY DISPLAY="${DISPLAY:-:0}" /usr/bin/rofi "$@"; }

WALLPAPER_DIR="$HOME/wallpapers"
CURRENT_LINK="$HOME/.config/qtile/current-wallpaper"
MODE="fill"

[ -d "$WALLPAPER_DIR" ] || { notify-send "Wallpaper" "No $WALLPAPER_DIR"; exit 1; }

current=$(readlink -f "$CURRENT_LINK" 2>/dev/null)

# Build the menu: one row per image, with a thumbnail and a bullet on the
# active one. rofi's dmenu icon protocol is  <label>\0icon\x1f<path>
menu=""
while IFS= read -r img; do
    name=$(basename "$img")
    [ "$(readlink -f "$img")" = "$current" ] && bullet="●" || bullet="○"
    menu+=$(printf '%s %s\0icon\x1f%s' "$bullet" "$name" "$img")$'\n'
done < <(find "$WALLPAPER_DIR" -maxdepth 1 -type f \
              \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \
                 -o -iname '*.webp' -o -iname '*.bmp' \) | sort)

[ -z "$menu" ] && { notify-send "Wallpaper" "No images in $WALLPAPER_DIR"; exit 1; }

ICON=$''  # nf-fa-image
choice=$(printf '%s' "$menu" | rofi -dmenu -i -p "Wallpaper" -mesg "$ICON" \
    -show-icons \
    -theme "$HOME/.config/rofi/menu.rasi" \
    -theme-str 'listview { columns: 3; lines: 3; }
                element-icon { size: 8em; }')

[ -z "$choice" ] && exit 0

selected="$WALLPAPER_DIR/${choice:2}"     # strip the "● " / "○ " prefix
[ -f "$selected" ] || { notify-send "Wallpaper" "Not found: ${choice:2}"; exit 1; }

# Persist, then apply to every screen (set_wallpaper only hits one at a time).
ln -sfn "$selected" "$CURRENT_LINK"
for i in 0 1 2 3; do
    qtile cmd-obj -o screen "$i" -f set_wallpaper -a "$selected" "$MODE" \
        >/dev/null 2>&1 || break
done

notify-send "Wallpaper" "${choice:2}"
