from libqtile import widget, qtile
from libqtile.lazy import lazy
from keyboard_utils import get_layout, toggle_layout
from fan_status import FanStatus
from screen_recorder import get_recording_status_text, toggle_recording

import os
import sys
from pathlib import Path

# Add theme_switcher to path and import colors
sys.path.insert(0, str(Path.home() / ".config" / "qtile" / "theme_switcher"))
from current_colors import color_light, color_dark, color_error, color_lighter, color_middark

# Groupbox for workspace management
group_box = widget.GroupBox(
    fontsize=24,
    highlight_method="block",
    this_current_screen_border=color_middark, 
    block_highlight_text_color=color_light,  
    inactive=color_middark,                    
    active=color_light,                     
    disable_drag=True
)

# Spacer and system tray
spacer = widget.Spacer()
systray = widget.Systray()

# Separator widget (reusable)
def create_separator():
    return widget.Sep(foreground=color_light, linewidth=1, padding=20)

# Temperature widgets
temp_icon = widget.TextBox("\uef2b", foreground=color_light, fontsize=26)
temp_sensor = widget.ThermalSensor(
    foreground=color_light,
    threshold=90,
    foreground_alert=color_error
)

# Network widgets
net_icon = widget.TextBox(
    "\ueb01",
    foreground=color_light,
    fontsize=26,
    mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("alacritty -e fish -c 'nmtui'")},
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
    mouse_callbacks={
    	"Button1": lambda: qtile.cmd_spawn("alacritty -e fish -c 'htop'")
    }
)
ram_widget = widget.Memory(measure_mem="G", foreground=color_light)

# CPU widgets
cpu_icon = widget.TextBox("\ue28c", foreground=color_light, fontsize=26)
cpu_widget = widget.CPU(foreground=color_light, format="{load_percent}%", width=45)

# Volume widgets
volume_icon = widget.TextBox("\uf028", foreground=color_light, fontsize=26, mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("pavucontrol")})
volume_widget = widget.PulseVolume(foreground=color_light)

# Battery widgets
battery_icon = widget.TextBox("\uf242", foreground=color_light, fontsize=30)
battery_widget = widget.Battery(
    charge_char="*",
    format="{char} {percent:2.0%}",
    foreground=color_light,
    low_foreground=color_error,
    discharge_char=""
)

# Clock widgets
date_icon = widget.TextBox("\uf073", foreground=color_light, fontsize=26)
date_widget = widget.Clock(format="%d-%m", foreground=color_light)
time_widget = widget.Clock(format="%I:%M %p", foreground=color_light)

# Keyboard widget
keyboard_icon = widget.TextBox("\uf11c", foreground=color_light, fontsize=26)
keyboard_widget = widget.GenPollText(
    update_interval=1, 
    func=lambda: get_layout(),
    mouse_callbacks={"Button1": lazy.function(toggle_layout)},
    foreground=color_light,
    padding=5
)

# Fan widget
fan_icon = widget.TextBox("\uefa7", foreground=color_light, fontsize=26)
fan_widget = FanStatus(foreground=color_light)

# Screen Recorder Widget
screen_recorder_icon = widget.TextBox("\uf03d", foreground=color_light, fontsize=26) # Changed text to REC and adjusted fontsize
screen_recorder_widget = widget.GenPollText(
    update_interval=1,
    func=lambda: get_recording_status_text(),
    mouse_callbacks={"Button1": lazy.function(lambda q: toggle_recording())},
    foreground=color_light,
    padding=5
)


def init_widgets_list():
    """Initialize and return the widgets list with all widgets"""
    widgets = [
        group_box,
        spacer,
        systray,
        create_separator(),
        fan_icon,
        fan_widget,
        create_separator(),
        temp_icon,
        temp_sensor,
        create_separator(),
        net_icon,
        net_widget,
        create_separator(),
        ram_icon,
        ram_widget,
        create_separator(),
        cpu_icon,
        cpu_widget,
        create_separator(),
        volume_icon,
        volume_widget,
        create_separator(),
        battery_icon,
        battery_widget,
        create_separator(),
        date_icon,
        date_widget,
        time_widget,
        create_separator(),
        keyboard_icon,
        keyboard_widget,
        create_separator(),
        screen_recorder_icon,
        screen_recorder_widget
    ]
    return widgets
