# dotfiles

My personal Linux desktop configuration. Everything here is what I actually use day to day — nothing included just for show.

## What's inside

**Window manager — Qtile**
Python-based tiling WM with a modular config split across dedicated files for keybindings, layouts, widgets, and colors. Nine workspaces with Nerd Font icons, vim-style navigation (hjkl), and a floating layout layer on top. Autostart handles the compositor, notifications, network applet, and monitor detection.

**Terminal — Alacritty**
Minimal TOML config. Nord color scheme, Hack Nerd Font at 10pt.

**Shell — Fish**
Managed with Fisher. NVM integration for Node version switching, pnpm and bun on PATH.

**Editor — Neovim**
NvChad as the base with custom plugin specs layered on top. LSP configured for Python and TypeScript via Mason.

**Compositor — Picom**
Rounded corners, transparency, animations, and blur. Mostly for aesthetics.

**Launcher — Rofi**
Nord-themed, keyboard-driven. Replaces dmenu entirely.

**Notifications — Dunst**
Positioned top-right, themed to match the active palette.

## Installation

No install script. Clone the repo and symlink (or copy) the directories you want into `~/.config/`:

```bash
git clone https://github.com/Chriscaracach/dotfiles.git
ln -s ~/path/to/dotfiles/qtile ~/.config/qtile
# repeat for nvim, fish, alacritty, etc.
```

Fonts required: **Hack Nerd Font** (for Qtile widgets, Alacritty, and Neovim icons).

## On open source

These configs are public because I've learned a lot from other people's dotfiles and it felt right to give back. Feel free to take whatever's useful. If you find a bug or have a suggestion, open an issue — I'm open to feedback.

This isn't meant to be a distribution or a one-size-fits-all setup. It's opinionated and built for how I work, but the modular structure makes it easy to swap out the parts you don't want.
