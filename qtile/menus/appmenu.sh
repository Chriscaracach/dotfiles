#!/bin/bash

# rofi's Wayland backend segfaults under qtile 0.37 (mmap of size 0 -> crash
# inside rofi's own g_log warning path, during the startup roundtrip). It is
# not caused by our config: it reproduces with wl_input_rules disabled.
# Running rofi through XWayland avoids it.
#
# Scoped to the rofi call ONLY. Unsetting WAYLAND_DISPLAY for the whole script
# breaks `qtile cmd-obj`, whose IPC socket name is derived from WAYLAND_DISPLAY
# (libqtile/ipc.py:38) - that silently stopped theme.sh from reloading the bar.
rofi() { env -u WAYLAND_DISPLAY DISPLAY="${DISPLAY:-:0}" /usr/bin/rofi "$@"; }

# Inject a static textbox widget at the top of mainbox so the Arch
# glyph (nf-linux-archlinux, U+F303) shows in drun mode. -mesg doesn't
# render reliably with -show drun, so we bake the icon into the theme.
rofi -show drun \
    -theme "$HOME/.config/rofi/menu.rasi" \
    -theme-str 'mainbox {
                  children: [textbox-arch, inputbar, listview];
                  spacing: 10px;
                }
                textbox-arch {
                  content: "";
                  font: "Hack Nerd Font Mono 44";
                  text-color: #88c0d0;
                  horizontal-align: 0.5;
                  vertical-align: 0.5;
                  padding: 0px;
                  background-color: transparent;
                }'
