#!/bin/bash
# Output switching for the Wayland session.
#
# Two qtile-Wayland quirks this works around, both found by testing on
# 2026-08-29 against qtile 0.37.0:
#
#  1. qtile rejects any output configuration containing a disabled head
#     (libqtile/backend/wayland/qw/server.c:235). kanshi TESTS a config before
#     applying and gives up when the test fails, so `output eDP-1 disable` in
#     kanshi's config silently does nothing while `kanshictl status` still
#     reports the profile as applied. wlr-randr does not test first, so it
#     works. kanshi therefore only detects; this script applies.
#
#  2. Even via wlr-randr, combining an enable and a disable in ONE invocation
#     is unreliable - it returns exit 0 and does nothing. Enabling and
#     disabling must be separate calls, disables last.
#
# qtile also (correctly) refuses to disable the last enabled output, so the
# enable always has to land before the disable.
#
# Connector names are the Wayland ones: HDMI-A-1, not xrandr's HDMI-1.

set -eu

INTERNAL="eDP-1"
EXTERNAL="HDMI-A-1"
MODE_1080="1920x1080"
STATE="${XDG_RUNTIME_DIR:-/tmp}/qtile-monitor-mode"

connected() { wlr-randr 2>/dev/null | grep -q "^${1} "; }
enabled()   { wlr-randr 2>/dev/null | awk -v o="$1" '/^[A-Za-z]/{n=$1} /Enabled:/{if(n==o) print $2}'; }

enable_at() {
    local tries=0
    while [ "$(enabled "$1")" != "yes" ] && [ $tries -lt 5 ]; do
        wlr-randr --output "$1" --on --mode "$MODE_1080" --pos "$2" || true
        tries=$((tries + 1)); sleep 0.4
    done
    # Position may need setting even when the output is already enabled.
    wlr-randr --output "$1" --on --mode "$MODE_1080" --pos "$2" || true
}

# A disable issued right after an enable is dropped by qtile roughly half the
# time - exit 0, no effect. Retrying converges (observed: 1-2 extra attempts).
disable() {
    local tries=0
    while [ "$(enabled "$1")" = "yes" ] && [ $tries -lt 6 ]; do
        wlr-randr --output "$1" --off || true
        tries=$((tries + 1)); sleep 0.4
    done
    [ "$(enabled "$1")" = "yes" ] && echo "warning: could not disable $1" >&2 || true
}

apply() {  # $1 = mode name, then: enable wanted outputs, THEN disable the rest
    case "$1" in
        docked)
            enable_at "$EXTERNAL" 0,0
            disable "$INTERNAL"
            ;;
        dual)
            enable_at "$INTERNAL" 0,0
            enable_at "$EXTERNAL" 1920,0
            ;;
        laptop)
            enable_at "$INTERNAL" 0,0
            connected "$EXTERNAL" && disable "$EXTERNAL"
            ;;
    esac
    echo "$1" > "$STATE"
}

cycle() {
    if ! connected "$EXTERNAL"; then
        apply laptop
        notify-send "Display" "Laptop only (no external connected)"
        return
    fi
    case "$(cat "$STATE" 2>/dev/null || echo laptop)" in
        docked) apply dual;   notify-send "Display" "Dual — laptop + external" ;;
        dual)   apply laptop; notify-send "Display" "Laptop only" ;;
        *)      apply docked; notify-send "Display" "External only" ;;
    esac
}

case "${1:-cycle}" in
    docked|dual|laptop) apply "$1" ;;
    cycle)  cycle ;;
    auto)   if connected "$EXTERNAL"; then apply docked; else apply laptop; fi ;;
    status) cat "$STATE" 2>/dev/null || echo unknown ;;
    *) echo "usage: $0 {docked|dual|laptop|cycle|auto|status}" >&2; exit 1 ;;
esac
