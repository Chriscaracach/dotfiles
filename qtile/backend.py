"""Backend detection.

The single place the X11/Wayland split is decided. Everything else in this
config imports IS_WAYLAND from here rather than sniffing the environment.

qtile.core.name is "wayland" or "x11". Before libqtile.init() runs — during
`qtile check`, for instance — the placeholder core reports None, so this
safely evaluates to False and the X11 path is assumed.

NOTE: qtile puts this directory on sys.path (confreader.py:117), so module
names here shadow stdlib ones. Do not name anything in this folder after a
stdlib module — `platform.py` would break widget.Battery, which imports it.
"""

from libqtile import qtile

IS_WAYLAND = qtile.core.name == "wayland"
