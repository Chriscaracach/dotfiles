from libqtile import layout
from libqtile.config import Match


def init_layouts(color_dark, color_light):
    layouts = [
        layout.Columns(
            border_focus_stack=[color_dark, color_dark],
            border_width=3,
            margin=4,
            border_normal=color_dark,
            border_focus=color_light,
        ),
        layout.Max(margin=2),
    ]

    floating_layout = layout.Floating(
        border_focus=color_light,
        border_normal=color_dark,
        border_width=3,
        float_rules=[
            *layout.Floating.default_float_rules,
            Match(wm_class="confirmreset"),  # gitk
            Match(wm_class="makebranch"),  # gitk
            Match(wm_class="maketag"),  # gitk
            Match(wm_class="ssh-askpass"),  # ssh-askpass
            Match(title="branchdialog"),  # gitk
            Match(title="pinentry"),  # GPG key password entry
        ],
    )
    return layouts, floating_layout
