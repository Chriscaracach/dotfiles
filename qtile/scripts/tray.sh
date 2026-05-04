#!/bin/bash
export DISPLAY="${DISPLAY:-:0}"

ICON=$''  # nf-fa-cog

choice=$(printf '%s\n' \
    "Slack" \
    "Discord" \
    "Network" \
    "Drata Agent" \
    "Flameshot" \
    "Volume" \
    | rofi -dmenu -i -p "Tray" -mesg "$ICON" -theme /home/chris/.config/rofi/menu.rasi)

case "$choice" in
    *Slack*)        setsid slack >/dev/null 2>&1 & ;;
    *Discord*)      setsid discord >/dev/null 2>&1 & ;;
    *Network*)      setsid nm-connection-editor >/dev/null 2>&1 & ;;
    *Drata*)        setsid drata-agent >/dev/null 2>&1 & ;;
    *Flameshot*)    setsid flameshot gui >/dev/null 2>&1 & ;;
    *Volume*)       setsid pavucontrol >/dev/null 2>&1 & ;;
esac
