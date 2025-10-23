# Qtile Theme Switcher

A modular theme switcher for Qtile that updates colors across multiple applications.

## Quick Start

### Switching Themes

Run the theme switcher:
```bash
~/.config/qtile/scripts/theme_switcher_new.py
```

Or switch to a specific theme directly:
```bash
~/.config/qtile/scripts/theme_switcher_new.py "Dark Grey"
```

## Adding New Themes

All themes are defined in `themes_config.py`. This file is designed to be easy to edit.

### Step 1: Define Your Theme

Open `themes_config.py` and add a new theme definition:

```python
MY_AWESOME_THEME = {
    "name": "My Awesome Theme",
    "color_dark": "#1a1a1a",      # Darkest shade
    "color_middark": "#2d2d2d",   # Medium dark shade
    "color_midlight": "#4a4a4a",  # Medium light shade
    "color_light": "#6b6b6b",     # Light shade
    "color_lighter": "#8c8c8c"    # Lightest shade
}
```

### Step 2: Register Your Theme

Add your theme to the `ALL_THEMES` list at the bottom of `themes_config.py`:

```python
ALL_THEMES = [
    WORK_CYAN,
    WORK_BLUE,
    PERSONAL_PURPLE,
    DARK_GREY,
    LIGHT_GREY,
    MY_AWESOME_THEME,  # Add your theme here
]
```

### Step 3: Use Your Theme

Run the theme switcher and your new theme will appear in the menu!

## Theme Structure

Each theme requires exactly 5 colors:

| Color | Purpose | Example |
|-------|---------|---------|
| `color_dark` | Darkest shade, used for backgrounds | `#2c2c2c` |
| `color_middark` | Medium dark, used for secondary backgrounds | `#4a4a4a` |
| `color_midlight` | Medium light, used for borders/accents | `#aeaeae` |
| `color_light` | Light shade, used for text/highlights | `#d8d8d8` |
| `color_lighter` | Lightest shade, used for bright accents | `#ffffff` |

## What Gets Updated

The theme switcher updates the following applications:

- **Qtile** - Window manager colors
- **Dunst** - Notification daemon
- **Rofi** - Application launcher
- **Alacritty** - Terminal emulator
- **Fish** - Shell prompt
- **Windsurf** - Code editor
- **Wallpaper** - Desktop background

## File Structure

```
theme_switcher/
├── themes_config.py    # Theme definitions (EDIT THIS!)
├── themes.py           # Theme loader (don't edit)
├── main.py             # Main switcher logic
├── qtile_colors.py     # Updates Qtile colors
├── dunst.py            # Updates Dunst config
├── rofi.py             # Updates Rofi config
├── alacritty.py        # Updates Alacritty config
├── fish.py             # Updates Fish shell
├── windsurf.py         # Updates Windsurf theme
├── wallpaper.py        # Updates wallpaper
├── services.py         # Restarts services
└── ui.py               # Rofi menu interface
```

## Tips

- **Organize themes**: Use the section comments in `themes_config.py` to group similar themes
- **Test colors**: Use a color picker to find hex codes that work well together
- **Backup**: Keep a backup of your favorite themes
- **Share**: Themes are just Python dictionaries, easy to share with others

## Troubleshooting

**Theme doesn't appear in menu:**
- Make sure it's added to the `ALL_THEMES` list
- Check that the theme dictionary has all 5 required colors
- Verify the "name" field is unique

**Colors look wrong:**
- Ensure hex codes start with `#`
- Use 6-digit hex codes (e.g., `#ffffff` not `#fff`)
- Check that colors are in quotes

**Theme switcher crashes:**
- Run with error output: `python ~/.config/qtile/scripts/theme_switcher_new.py`
- Check for syntax errors in `themes_config.py`
