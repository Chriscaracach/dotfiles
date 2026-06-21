# Dotfiles Setup Guide

Fresh Arch install → working desktop. Follow in order.

---

## 1. Base requirements

```bash
sudo pacman -S git base-devel xorg-server xorg-xinit
```

---

## 2. AUR helper

```bash
git clone https://aur.archlinux.org/yay.git
cd yay && makepkg -si
```

---

## 3. Qtile

### Packages
```bash
sudo pacman -S qtile python-pip
```

### Runtime dependencies (things qtile config calls)
```bash
sudo pacman -S \
  brightnessctl \        # brightness keys
  dunst \                # notifications
  picom \                # compositor
  nitrogen \             # wallpaper
  network-manager-applet \  # nm-connection-editor in tray menu
  flameshot \            # screenshot (mod+p and tray)
  pcmanfm \              # file manager (mod+g and tray)
  arandr \               # display config (tray)
  lxappearance \         # theme switcher (tray)
  xorg-setxkbmap \       # keyboard layout switching
  ffmpeg \               # screen recorder widget
  pipewire-pulse \       # pactl commands (volume + mic scripts)
  gnome-disk-utility     # Disks (tray)
```

### Post-install
- Set a wallpaper with nitrogen, then run `nitrogen --restore` (already in autostart)
- Qtile starts via `~/.xinitrc` or a display manager pointing to `qtile`

---

## 4. Rofi

### Packages
```bash
sudo pacman -S rofi
```

### Fonts (required for Nerd Font glyphs in menus)
```bash
sudo pacman -S ttf-hack-nerd
```

### Notes
- `mod+space` → app launcher (`~/.config/qtile/menus/appmenu.sh`)
- `mod+v` → mic control (`~/.config/qtile/menus/mic.sh`)
- `mod+i` → AI prompt (`~/.config/qtile/menus/ai.sh`)
- All menus use `~/.config/rofi/menu.rasi`

---

## 5. Alacritty

```bash
sudo pacman -S alacritty
```

No extra dependencies. Config lives in `~/.config/alacritty/`.

---

## 6. Dunst

```bash
sudo pacman -S dunst
```

Font used: `Hack Nerd Font Mono` — covered by `ttf-hack-nerd` above.

---

## 7. Fish

### Packages
```bash
sudo pacman -S fish
chsh -s /usr/bin/fish   # set as default shell
```

### Plugin manager
```bash
curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source && fisher install jorgebucaran/fisher
```

### Plugins
```bash
fisher install jorgebucaran/nvm.fish
```

### Node (used in config.fish)
```bash
nvm install v22.22.2
nvm use v22.22.2
```

### Other tools referenced in config.fish
```bash
# pnpm
curl -fsSL https://get.pnpm.io/install.sh | sh

# bun
curl -fsSL https://bun.sh/install | bash
```

---

## 8. Tmux

### Packages
```bash
sudo pacman -S tmux
```

### Config location
Tmux doesn't read from `~/.config/` — copy or symlink the config to the home directory:

```bash
ln -s ~/path/to/dotfiles/tmux/tmux.conf ~/.tmux.conf
```

### Plugin manager (tpm)
```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

Start tmux and press `prefix + I` (Alt+Space, then Shift+i) to install plugins.

---

## 9. Neovim (NvChad)

### Packages
```bash
sudo pacman -S neovim git gcc make
```

### NvChad (the distro used)
```bash
git clone https://github.com/NvChad/starter ~/.config/nvim
nvim   # triggers lazy.nvim bootstrap on first launch
```

> **Note:** The `~/.config/nvim` folder from dotfiles already has the full config.
> Skip the clone above if restoring from dotfiles — just run `nvim` and let lazy sync.

---

## 10. PCManFM

```bash
sudo pacman -S pcmanfm
```

No extra config needed beyond what's in `~/.config/pcmanfm/`.

---

## 11. Picom

```bash
sudo pacman -S picom
```

Config uses:
- `backend = "glx"` — requires a working GPU driver
- `animations = true` — supported natively in picom v13+
- `corner-radius = 8` — native, no fork needed

---

## 12. Fonts summary

All at once:

```bash
sudo pacman -S \
  ttf-hack-nerd \
  noto-fonts \
  noto-fonts-emoji \
  noto-fonts-extra
```

---

## 13. Display manager (optional)

The config uses `ly`:

```bash
sudo pacman -S ly
sudo systemctl enable ly
```

Or use `startx` with an `~/.xinitrc` containing:

```bash
exec qtile start
```

---

## Themes

Themes live in `~/.config/themes/<name>/` — six color files each (qtile, alacritty, rofi, dunst, fish, tmux). The active theme is just a symlink, which the configs import from:

```bash
ln -s ~/.config/themes/nord ~/.config/themes/current
```

Switch from the rofi menu with `mod+u` (`qtile/menus/theme.sh`) — it flips the symlink and live-reloads everything. Dunst picks its colors up through the `dunst/dunstrc.d/99-theme.conf` drop-in symlink (already in the repo).

To add a theme: copy an existing theme folder, change the hex values, done.

---

## Quick full install (copy-paste)

```bash
sudo pacman -S \
  qtile python-pip \
  rofi alacritty dunst picom nitrogen \
  network-manager-applet pcmanfm arandr lxappearance \
  flameshot brightnessctl ffmpeg \
  pipewire-pulse gnome-disk-utility xorg-setxkbmap \
  fish tmux neovim git gcc make \
  ttf-hack-nerd noto-fonts noto-fonts-emoji noto-fonts-extra \
  ly

# Fisher
curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source && fisher install jorgebucaran/fisher
fisher install jorgebucaran/nvm.fish
nvm install v22.22.2
```

---

## After restoring dotfiles

1. `chsh -s /usr/bin/fish`
2. Run `nvim` once to trigger plugin sync
3. Symlink `tmux/tmux.conf` to `~/.tmux.conf`, clone tpm, then `prefix + I` inside tmux
4. `ln -s ~/.config/themes/nord ~/.config/themes/current` (or any theme)
5. Run `nitrogen --restore` or pick a wallpaper
6. `sudo systemctl enable --now NetworkManager`
7. Reboot or `startx`
