#!/bin/bash
export DISPLAY="${DISPLAY:-:0}"

THEMES_DIR="$HOME/.config/themes"
CURRENT_LINK="$THEMES_DIR/current"

# Collect available themes (every directory except the `current` symlink)
themes=()
for d in "$THEMES_DIR"/*/; do
    name=$(basename "$d")
    [ "$name" = "current" ] && continue
    themes+=("$name")
done
[ ${#themes[@]} -eq 0 ] && exit 1

current=$(basename "$(readlink "$CURRENT_LINK" 2>/dev/null)")

# Build menu with a bullet on the active theme
menu=()
for t in "${themes[@]}"; do
    [ "$t" = "$current" ] && menu+=("● $t") || menu+=("○ $t")
done

ICON=$''  # nf-fa-paint_brush
choice=$(printf '%s\n' "${menu[@]}" | rofi -dmenu -i -p "Theme" -mesg "$ICON" -theme "$HOME/.config/rofi/menu.rasi")
[ -z "$choice" ] && exit 0

theme="${choice:2}"
[ "$theme" = "$current" ] && exit 0

# The switch itself: one symlink flip
ln -sfn "$THEMES_DIR/$theme" "$CURRENT_LINK"

# Dunst reads its colors through a drop-in symlink — make sure it exists
mkdir -p "$HOME/.config/dunst/dunstrc.d"
ln -sfn ../../themes/current/dunst.conf "$HOME/.config/dunst/dunstrc.d/99-theme.conf"

# Apply to running apps
qtile cmd-obj -o cmd -f reload_config
dunstctl reload
touch "$HOME/.config/alacritty/alacritty.toml"  # trigger alacritty live reload
fish -c "set -U __theme_active '$theme'"  # fires the reload handler in every open fish
tmux source-file ~/.tmux.conf 2>/dev/null

notify-send "Theme" "$theme"
