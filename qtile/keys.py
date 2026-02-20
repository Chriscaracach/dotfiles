import os
from libqtile.config import Key
from libqtile.lazy import lazy


def init_keys(mod, terminal, groups):
    keys = [
        # Window management keybindings
        Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
        Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
        Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
        Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
        Key(
            [mod, "shift"],
            "h",
            lazy.layout.shuffle_left(),
            desc="Move window to the left",
        ),
        Key(
            [mod, "shift"],
            "l",
            lazy.layout.shuffle_right(),
            desc="Move window to the right",
        ),
        Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
        Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
        Key(
            [mod, "control"],
            "h",
            lazy.layout.grow_left(),
            desc="Grow window to the left",
        ),
        Key(
            [mod, "control"],
            "l",
            lazy.layout.grow_right(),
            desc="Grow window to the right",
        ),
        Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
        Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
        Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
        Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
        Key(
            [mod],
            "f",
            lazy.window.toggle_fullscreen(),
            desc="Toggle fullscreen on the focused window",
        ),
        Key(
            [mod, "shift"],
            "f",
            lazy.window.toggle_floating(),
            desc="Toggle floating on the focused window",
        ),
        # Brightness
        Key(
            [mod], "k", lazy.spawn("brightnessctl set +10%"), desc="Increase brightness"
        ),
        Key(
            [mod], "l", lazy.spawn("brightnessctl set 10%-"), desc="Decrease brightness"
        ),
        # Launchers / Killers
        Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
        Key([mod], "space", lazy.spawn("rofi -show drun"), desc="Launch rofi"),
        Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
        Key([mod], "p", lazy.spawn("flameshot gui"), desc="Launch Flameshot"),
        Key(
            [mod, "shift"],
            "p",
            lazy.spawn(os.path.expanduser("~/prs.sh")),
            desc="Show pending PRs",
        ),
        Key(
            [mod, "shift"],
            "j",
            lazy.spawn(
                "alacritty -e /home/chriscodingit/jarvis_assistant/venv/bin/python /home/chriscodingit/jarvis_assistant/jarvis.py"
            ),
            desc="Run Jarvis Assistant",
        ),
        Key(
            [mod, "shift"],
            "o",
            lazy.spawn(os.path.expanduser("~/my_prs.sh")),
            desc="Show my PRs",
        ),
        Key(
            [mod],
            "e",
            lazy.spawn("/home/chriscodingit/env-runner.sh"),
            desc="Run environments",
        ),
        Key(
            [mod],
            "t",
            lazy.spawn(
                "python3 /home/chriscodingit/.config/qtile/scripts/theme_switcher_new.py"
            ),
            desc="Launch theme switcher",
        ),
        # General
        Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
        Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    ]

    # Group shortcuts
    keys.append(Key([mod], "c", lazy.group["1"].toscreen()))
    keys.append(Key([mod], "z", lazy.group["2"].toscreen()))
    keys.append(Key([mod], "a", lazy.group["4"].toscreen()))
    keys.append(Key([mod], "d", lazy.group["6"].toscreen()))
    keys.append(Key([mod], "x", lazy.group["7"].toscreen()))
    keys.append(Key([mod], "s", lazy.group["8"].toscreen()))
    keys.append(Key([mod], "m", lazy.group["9"].toscreen()))

    for i in groups:
        keys.extend(
            [
                Key(
                    [mod],
                    i.name,
                    lazy.group[i.name].toscreen(),
                    desc=f"Switch to group {i.name}",
                ),
                Key(
                    [mod, "shift"],
                    i.name,
                    lazy.window.togroup(i.name, switch_group=True),
                    desc=f"Switch to & move focused window to group {i.name}",
                ),
            ]
        )

    return keys
