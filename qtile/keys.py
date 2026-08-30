import os

from libqtile import qtile
from libqtile.config import Key
from libqtile.lazy import lazy

from backend import IS_WAYLAND


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
        # Launchers / Killers
        Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
        Key(
            [mod],
            "space",
            lazy.spawn(f"bash {os.path.expanduser('~/.config/qtile/menus/appmenu.sh')}"),
            desc="Launch rofi",
        ),
        Key(
            [mod],
            "v",
            lazy.spawn(f"bash {os.path.expanduser('~/.config/qtile/menus/mic.sh')}"),
            desc="Mic control",
        ),
        Key(
            [mod],
            "i",
            lazy.spawn(f"bash {os.path.expanduser('~/.config/qtile/menus/ai.sh')}"),
            desc="AI prompt",
        ),
        Key(
            [mod],
            "u",
            lazy.spawn(f"bash {os.path.expanduser('~/.config/qtile/menus/theme.sh')}"),
            desc="Theme switcher",
        ),
        Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
        Key(
            [mod],
            "w",
            lazy.spawn(
                f"bash {os.path.expanduser('~/.config/qtile/menus/wallpaper.sh')}"
            ),
            desc="Wallpaper picker",
        ),
        # Cycle output layout: external only -> dual -> laptop only.
        # Wayland only; X11 keeps the xrandr scripts.
        Key(
            [mod],
            "o",
            lazy.spawn(
                f"bash {os.path.expanduser('~/.config/qtile/scripts/monitors.sh')} cycle"
            ).when(func=lambda: qtile.core.name == "wayland"),
            desc="Cycle monitor layout",
        ),
        Key(
            [mod],
            "p",
            lazy.spawn(
                f"sh {os.path.expanduser('~/.config/qtile/scripts/screenshot.sh')}"
                if IS_WAYLAND
                else "flameshot gui"
            ),
            desc="Region screenshot",
        ),
        Key(
            [mod],
            "g",
            lazy.spawn("pcmanfm"),
            desc="Launch file manager",
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

    # Wayland does not handle Ctrl+Alt+F<n> for you the way the kernel does on a
    # text console or X does in a session — the compositor holds the keyboard, so
    # the VT switch must be bound explicitly or there is no way out of the
    # session. Harmless on X11: .when() defers the backend check to press time,
    # and there it never fires.
    for vt in range(1, 8):
        keys.append(
            Key(
                ["control", "mod1"],
                f"f{vt}",
                lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
                desc=f"Switch to VT{vt}",
            )
        )

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
