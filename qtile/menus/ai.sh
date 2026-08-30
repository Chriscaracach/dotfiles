#!/usr/bin/env bash

# rofi's Wayland backend segfaults under qtile 0.37 (mmap of size 0 -> crash
# inside rofi's own g_log warning path, during the startup roundtrip). It is
# not caused by our config: it reproduces with wl_input_rules disabled.
# Running rofi through XWayland avoids it.
#
# Scoped to the rofi call ONLY. Unsetting WAYLAND_DISPLAY for the whole script
# breaks `qtile cmd-obj`, whose IPC socket name is derived from WAYLAND_DISPLAY
# (libqtile/ipc.py:38) - that silently stopped theme.sh from reloading the bar.
rofi() { env -u WAYLAND_DISPLAY DISPLAY="${DISPLAY:-:0}" /usr/bin/rofi "$@"; }

PROMPT=$(rofi -dmenu \
  -p "" \
  -lines 0 \
  -no-fixed-num-lines \
  -theme "$HOME/.config/rofi/menu.rasi" \
  -theme-str 'window { width: 700px; }
              mainbox { children: [inputbar]; }
              entry { placeholder: "Ask AI..."; }
              listview { enabled: false; }')

[ -z "$PROMPT" ] && exit

alacritty --title tgpt-sky -e bash -c "
tgpt --provider sky --interactive \"$PROMPT\" 2>/dev/null || tgpt --provider sky \"$PROMPT\";
exec bash
"
