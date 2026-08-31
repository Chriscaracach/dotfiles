#!/bin/sh
# Install these dotfiles into the CURRENT user's home. Idempotent: safe to
# re-run after a `git pull`, and a no-op for anything already linked.
#
# Usage, from anywhere:
#     sh ~/prog/dotfiles/bin/install.sh            # link everything
#     sh ~/prog/dotfiles/bin/install.sh --dry-run  # show what it would do
#
# Everything is symlinked back into this clone, so `git pull` updates the live
# config with no copying step. Each user gets their OWN clone - the theme
# switcher (mod+u) and wallpaper picker (mod+w) persist their choice as
# symlinks written *inside* the config dirs, so a shared read-only copy would
# break both. Those two state symlinks are gitignored.
#
# Anything already present that is not the right symlink is moved aside to
# <name>.bak-<timestamp> rather than deleted.

set -eu

DOTFILES=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}"
STAMP=$(date +%Y%m%d-%H%M%S)
SHARED_WALLPAPERS=/usr/local/share/wallpapers
DEFAULT_THEME=nord

DRY=0
[ "${1:-}" = "--dry-run" ] && DRY=1

say()  { printf '%s\n' "$*"; }
run()  { if [ "$DRY" = 1 ]; then printf '  would: %s\n' "$*"; else eval "$@"; fi; }

# link <source-in-repo> <target-in-home>
link() {
    src=$DOTFILES/$1
    dst=$2

    [ -e "$src" ] || { say "  skip   ${dst#$HOME/}  (no $1 in repo)"; return 0; }

    if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
        say "  ok     ${dst#$HOME/}"
        return 0
    fi

    run "mkdir -p '$(dirname "$dst")'"
    if [ -e "$dst" ] || [ -L "$dst" ]; then
        say "  backup ${dst#$HOME/} -> ${dst##*/}.bak-$STAMP"
        run "mv '$dst' '$dst.bak-$STAMP'"
    fi
    say "  link   ${dst#$HOME/} -> $1"
    run "ln -s '$src' '$dst'"
}

# copy_if_absent <source-in-repo> <target-in-home> <why>
# For files the user is expected to diverge on, or that the app rewrites in
# place - symlinking those would push churn (or someone else's identity) into
# the repo.
copy_if_absent() {
    src=$DOTFILES/$1
    dst=$2

    [ -e "$src" ] || return 0
    if [ -e "$dst" ]; then
        say "  keep   ${dst#$HOME/}  (yours; $3)"
        return 0
    fi
    say "  copy   ${dst#$HOME/}  ($3)"
    run "mkdir -p '$(dirname "$dst")'"
    run "cp '$src' '$dst'"
}

say "dotfiles: $DOTFILES"
say "home:     $HOME"
[ "$DRY" = 1 ] && say "(dry run - nothing will be written)"

# --- XDG config directories -------------------------------------------------
say ""
say "config directories:"
for d in alacritty dunst kanshi lazygit nvim pcmanfm picom qtile rofi themes \
         xdg-desktop-portal; do
    link "$d" "$CONFIG/$d"
done

# --- fish -------------------------------------------------------------------
# Linked entry by entry, not as one directory: fish rewrites fish_variables
# constantly (universal vars, incl. the __theme_active the theme switcher
# pokes), and a symlinked dir would turn every shell into repo churn.
say ""
say "fish:"
for f in config.fish fish_plugins completions conf.d functions; do
    link "fish/$f" "$CONFIG/fish/$f"
done
copy_if_absent fish/fish_variables "$CONFIG/fish/fish_variables" "fish rewrites this"

# --- files outside ~/.config ------------------------------------------------
say ""
say "home files:"
link tmux/tmux.conf "$HOME/.tmux.conf"
link bin/startw     "$HOME/.local/bin/startw"
link xinitrc        "$HOME/.xinitrc"
# Not symlinked: it carries a name and email. Copied as a starting point only.
copy_if_absent git/gitconfig "$HOME/.gitconfig" "set your own user.name/user.email"

# --- per-user state the configs expect --------------------------------------
# Both of these are gitignored symlinks that live inside the linked config
# dirs; the switchers rewrite them, so they are per-user, not repo content.
say ""
say "per-user state:"

if [ -L "$CONFIG/themes/current" ] || [ -e "$CONFIG/themes/current" ]; then
    say "  ok     themes/current -> $(basename "$(readlink -f "$CONFIG/themes/current")")"
else
    theme=$DEFAULT_THEME
    [ -d "$DOTFILES/themes/$theme" ] || theme=$(ls "$DOTFILES/themes" | head -n1)
    say "  link   themes/current -> $theme"
    run "ln -sfn '$CONFIG/themes/$theme' '$CONFIG/themes/current'"
fi

# dunst reads its colors through this drop-in. It is tracked in the repo, so
# the dunst link above normally provides it; recreated here for a partial run.
if [ ! -L "$CONFIG/dunst/dunstrc.d/99-theme.conf" ]; then
    say "  link   dunst/dunstrc.d/99-theme.conf"
    run "mkdir -p '$CONFIG/dunst/dunstrc.d'"
    run "ln -sfn ../../themes/current/dunst.conf '$CONFIG/dunst/dunstrc.d/99-theme.conf'"
fi

# Wallpapers are shared between users at $SHARED_WALLPAPERS (73M of images is
# not worth duplicating per account, and /home/<user> is mode 700 so one user's
# copy is unreadable to the other). See SETUP.md for populating it.
if [ -e "$HOME/wallpapers" ]; then
    say "  ok     wallpapers"
elif [ -d "$SHARED_WALLPAPERS" ]; then
    say "  link   wallpapers -> $SHARED_WALLPAPERS"
    run "ln -s '$SHARED_WALLPAPERS' '$HOME/wallpapers'"
else
    say "  make   wallpapers  (empty; $SHARED_WALLPAPERS does not exist)"
    run "mkdir -p '$HOME/wallpapers'"
fi

# config.py falls back to a fixed filename when this has never been set; point
# it at whatever is actually there so the first session has a wallpaper.
if [ ! -L "$CONFIG/qtile/current-wallpaper" ]; then
    first=$(find -L "$HOME/wallpapers" -maxdepth 1 -type f \
            \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \
               -o -iname '*.webp' -o -iname '*.bmp' \) 2>/dev/null | sort | head -n1)
    if [ -n "$first" ]; then
        say "  link   qtile/current-wallpaper -> $(basename "$first")"
        run "ln -sfn '$first' '$CONFIG/qtile/current-wallpaper'"
    else
        say "  skip   qtile/current-wallpaper  (no images in ~/wallpapers yet)"
    fi
fi

say ""
say "Done. Start the Wayland session from a TTY with:  startw"
say "(X11 fallback: startx)"
