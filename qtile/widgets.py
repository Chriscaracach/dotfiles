import re
import subprocess

from libqtile import widget, qtile
from libqtile.lazy import lazy
from keyboard_utils import get_layout, toggle_layout

# from fan_status import FanStatus
from screen_recorder import get_recording_status_text, toggle_recording

from pathlib import Path

from colors import (
    color_light,
    color_dark,
    color_red,
    color_middark,
    color_bg,
)

# Groupbox for workspace management
group_box = widget.GroupBox(
    font="Hack Nerd Font Mono",
    fontsize=24,
    highlight_method="block",
    this_current_screen_border=color_middark,
    block_highlight_text_color=color_light,
    inactive=color_middark,
    active=color_light,
    disable_drag=True,
)

# Temperature widgets
temp_icon = widget.TextBox(
    "\uf2cb",
    foreground=color_light,
    fontsize=26,
)
temp_sensor = widget.ThermalSensor(
    foreground=color_light,
    threshold=90,
    foreground_alert=color_red,
)

# Network widgets
net_icon = widget.TextBox(
    "\ueb01",
    foreground=color_light,
    fontsize=26,
    mouse_callbacks={
        "Button1": lambda: qtile.spawn("alacritty -e fish -c 'nmtui'")
    },
)
net_widget = widget.Net(
    foreground=color_light,
    format="{down:.0f}{down_suffix:<2} ↓↑ {up:.0f}{up_suffix:<2}",
    width=110,
)

# RAM widgets
ram_icon = widget.TextBox(
    "\uefc5",
    foreground=color_light,
    fontsize=26,
    mouse_callbacks={"Button1": lambda: qtile.spawn("alacritty -e fish -c 'htop'")},
)
ram_widget = widget.Memory(
    measure_mem="G",
    foreground=color_light,
)

# CPU widgets
cpu_icon = widget.TextBox(
    "\uec19",
    foreground=color_light,
    fontsize=26,
)
cpu_widget = widget.CPU(
    foreground=color_light,
    format="{load_percent}%",
    width=45,
)

# Volume widgets
def get_volume_text():
    try:
        muted = "yes" in subprocess.check_output(
            ["pactl", "get-sink-mute", "@DEFAULT_SINK@"], text=True
        )
        vol_out = subprocess.check_output(
            ["pactl", "get-sink-volume", "@DEFAULT_SINK@"], text=True
        )
        match = re.search(r"(\d+)%", vol_out)
        vol = int(match.group(1)) if match else 0

        filled = round(vol * 8 / 100)
        bar = "█" * filled + "░" * (8 - filled)
        prefix = "M " if muted else ""
        return f"{prefix}{bar} {vol}%"
    except Exception:
        return "?%"


def _vol_up(_):
    subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"])
    volume_widget.tick()


def _vol_down(_):
    subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"])
    volume_widget.tick()


_volume_callbacks = {
    "Button1": lambda: qtile.spawn("pavucontrol"),
    "Button4": lazy.function(_vol_up),
    "Button5": lazy.function(_vol_down),
}
volume_icon = widget.TextBox(
    "\uf028",
    foreground=color_light,
    fontsize=26,
    mouse_callbacks=_volume_callbacks,
)
volume_widget = widget.GenPollText(
    update_interval=1,
    func=get_volume_text,
    foreground=color_light,
    mouse_callbacks=_volume_callbacks,
    padding=5,
)

# Battery widgets
battery_icon = widget.TextBox(
    "\uf242",
    foreground=color_light,
    fontsize=30,
)
battery_widget = widget.Battery(
    charge_char="*",
    format="{char} {percent:2.0%}",
    foreground=color_light,
    low_foreground=color_red,
    discharge_char="",
)

# Clock widgets
date_icon = widget.TextBox(
    "\ueab0",
    foreground=color_light,
    fontsize=26,
)
date_widget = widget.Clock(
    format="%d-%m",
    foreground=color_light,
)
time_widget = widget.Clock(
    format="%I:%M %p",
    foreground=color_light,
)

# Keyboard widget
keyboard_icon = widget.TextBox(
    "\uf11c",
    foreground=color_light,
    fontsize=26,
)
keyboard_widget = widget.GenPollText(
    update_interval=1,
    func=lambda: get_layout(),
    mouse_callbacks={"Button1": lazy.function(toggle_layout)},
    foreground=color_light,
    padding=5,
)


# Screen Recorder Widget
screen_recorder_icon = widget.TextBox(
    "\uead9",
    foreground=color_light,
    fontsize=26,
)
screen_recorder_widget = widget.GenPollText(
    update_interval=1,
    func=lambda: get_recording_status_text(),
    mouse_callbacks={"Button1": lazy.function(lambda q: toggle_recording())},
    foreground=color_light,
    padding=5,
)

# Spacer widget
spacer = widget.Spacer()

# Separator widget
separator = widget.Sep(
    linewidth=1,
    padding=10,
    foreground=color_middark,
)


def init_widgets_list():
    """Initialize and return the widgets list with all widgets"""
    widgets = [
        group_box,
        spacer,
        temp_icon,
        temp_sensor,
        separator,
        net_icon,
        net_widget,
        separator,
        ram_icon,
        ram_widget,
        separator,
        cpu_icon,
        cpu_widget,
        separator,
        volume_icon,
        volume_widget,
        separator,
        battery_icon,
        battery_widget,
        separator,
        date_icon,
        date_widget,
        separator,
        time_widget,
        separator,
        keyboard_icon,
        keyboard_widget,
        separator,
        screen_recorder_icon,
        screen_recorder_widget,
    ]
    return widgets
