<img width="300" height="220" alt="WhatsApp Image 2026-05-10 at 7 43 59 PM" src="https://github.com/user-attachments/assets/759fdb64-7360-4a67-aae7-4b95dd7e4d04" />

# Dotfiles

My personal Linux desktop configuration. Everything here is what I actually use day to day — nothing included just for show.

## What's inside

**Window manager — Qtile**
Python-based tiling WM with a modular config split across dedicated files for keybindings, layouts, widgets, and colors. Nine workspaces with Nerd Font icons, vim-style navigation (hjkl), and a floating layout layer on top. Autostart handles the compositor, notifications, network applet, and monitor detection.

**Terminal — Alacritty**
Minimal TOML config. Nord color scheme, Hack Nerd Font at 10pt.

**Shell — Fish**
Managed with Fisher. NVM integration for Node version switching, pnpm and bun on PATH.

**Multiplexer — Tmux**
Alt+Space prefix, vim-style pane resizing, status bar on top with CPU/memory monitor. Plugins managed with tpm.

**Editor — Neovim**
NvChad as the base with custom plugin specs layered on top. LSP configured for Python and TypeScript via Mason.

**Compositor — Picom**
Rounded corners, transparency, animations, and blur. Mostly for aesthetics.

**Launcher — Rofi**
Nord-themed, keyboard-driven. Replaces dmenu entirely.

**Notifications — Dunst**
Positioned top-right, themed to match the active palette.

**Theme switcher**
One rofi menu (`mod+u`) re-themes the whole desktop — Qtile, Alacritty, Rofi, Dunst, fish, and tmux — by flipping a single symlink (`~/.config/themes/current`). Every app imports its colors from that path natively, so there's no config rewriting and nothing to drift. Ships with Nord, Gruvbox, and Material Deep Ocean; adding a theme is just a new folder with six small color files.

## Installation

No install script. Clone the repo and symlink (or copy) the directories you want into `~/.config/`:

```bash
git clone https://github.com/Chriscaracach/dotfiles.git
ln -s ~/path/to/dotfiles/qtile ~/.config/qtile
# repeat for nvim, fish, alacritty, etc.
```

Tmux is the exception — its config lives at `~/.tmux.conf`:

```bash
ln -s ~/path/to/dotfiles/tmux/tmux.conf ~/.tmux.conf
```

Fonts required: **Hack Nerd Font** (for Qtile widgets, Alacritty, and Neovim icons).

## On open source

These configs are public because I've learned a lot from other people's dotfiles and it felt right to give back. Feel free to take whatever's useful. If you find a bug or have a suggestion, open an issue — I'm open to feedback.

This isn't meant to be a distribution or a one-size-fits-all setup. It's opinionated and built for how I work, but the modular structure makes it easy to swap out the parts you don't want.
