#!/bin/bash
export DISPLAY="${DISPLAY:-:0}"

# Get the input source name
source_name=$(pactl list sources short | grep -v monitor | awk '{print $2}' | head -1)
[ -z "$source_name" ] && exit 1

# Get mute state
is_muted=$(pactl get-source-mute "$source_name" 2>/dev/null | grep -c "yes")
[ "$is_muted" -eq 1 ] && mute_label="Unmute Mic" || mute_label="Mute Mic"

# Parse ports and active port from this source
eval "$(pactl list sources | awk -v src="$source_name" '
    /^\tName:/ && $2==src  { found=1 }
    found && /^\tPorts:/   { in_ports=1; next }
    found && /^\tActive Port:/ { printf "active_port=\"%s\";\n", $3; in_ports=0; next }
    found && /^\tFormats:/ { found=0 }
    found && in_ports && /^\t\t/ {
        sub(/^\t\t/, "")
        port_id = substr($0, 1, index($0, ":")-1)
        rest = substr($0, index($0, ": ")+2)
        sub(/ \(.*/, "", rest)
        printf "ports+=(\"%s\"); labels+=(\"%s\");\n", port_id, rest
    }
')"

# Build menu
menu=("$mute_label")
for i in "${!ports[@]}"; do
    [ "${ports[$i]}" = "$active_port" ] && bullet="●" || bullet="○"
    menu+=("$bullet ${labels[$i]}")
done

ICON=$''  # nf-fa-microphone
choice=$(printf '%s\n' "${menu[@]}" | rofi -dmenu -i -p "Mic" -mesg "$ICON" -theme /home/chris/.config/rofi/menu.rasi)
[ -z "$choice" ] && exit 0

if [ "$choice" = "$mute_label" ]; then
    pactl set-source-mute "$source_name" toggle
else
    chosen_label="${choice:2}"
    for i in "${!labels[@]}"; do
        if [ "${labels[$i]}" = "$chosen_label" ]; then
            pactl set-source-port "$source_name" "${ports[$i]}"
            pactl set-source-volume "$source_name" 30%
            break
        fi
    done
fi
