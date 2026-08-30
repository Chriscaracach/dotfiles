#!/bin/sh
# Wayland region screenshot: select with slurp, capture with grim, annotate
# with satty. The X11 session keeps using `flameshot gui` (see keys.py).

set -eu

OUT_DIR="$HOME/Screenshots"
mkdir -p "$OUT_DIR"
OUT="$OUT_DIR/$(date +%F-%H%M%S).png"

REGION=$(slurp) || exit 0   # empty selection / Esc => user cancelled

if command -v satty >/dev/null 2>&1; then
    grim -g "$REGION" - | satty \
        --filename - \
        --output-filename "$OUT" \
        --early-exit \
        --copy-command wl-copy
else
    # No annotation UI available: save and put it on the clipboard anyway.
    grim -g "$REGION" "$OUT"
    wl-copy < "$OUT"
    notify-send "Screenshot" "$(basename "$OUT")"
fi
