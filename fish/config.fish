if status is-interactive
    nvm use v22.22.2 
    # Commands to run in interactive sessions can go here
end

# pnpm
set -gx PNPM_HOME "$HOME/.local/share/pnpm"
if not string match -q -- $PNPM_HOME $PATH
  set -gx PATH "$PNPM_HOME" $PATH
end
# pnpm end

# bun
set --export BUN_INSTALL "$HOME/.bun"
set --export PATH $BUN_INSTALL/bin $PATH

fish_add_path ~/.local/bin


# Ensure system paths are first
set -gx PATH /usr/local/bin /usr/bin /bin /usr/local/sbin /usr/sbin /sbin $PATH

# Shell colors come from the active theme (switched via mod+u).
# Runs at startup, and again in every open shell when the theme switcher
# pokes the __theme_active universal variable.
function __apply_theme --on-variable __theme_active
    test -e ~/.config/themes/current/fish.fish
    and source ~/.config/themes/current/fish.fish
end
__apply_theme
