#!/bin/bash

preset=$1


# Utility functions

error_exit()
{
    echo "$1"
    exit 1
}

array_contains() {
    local numberOfParams=$#
    local value=${!numberOfParams}
    for ((i=1;i < numberOfParams;i++)) {
        if [ "${!i}" == "${value}" ]; then
            return 0
        fi
    }
    return 1
}


# Settings arrays
declare -A gnome_font_scale
declare -A gnome_icon_size
declare -A gnome_cursor_size
declare -A firefox_scale
declare -A chromium_scale


### EDIT HERE >>>

# User variables
firefox_profile_folder="" # Your firefox profile id

# Preset list
presets=(default 1080p14inch) # Specify your presets here

# Default preset
gnome_font_scale[default]="1.0"
gnome_icon_size[default]="32"
gnome_cursor_size[default]="24"
firefox_scale[default]="1.0"
chromium_scale[default]="1.0"

# 1080p, 14" laptop
gnome_font_scale[1080p14inch]="1.2"
gnome_icon_size[1080p14inch]="36"
gnome_cursor_size[1080p14inch]="32"
firefox_scale[1080p14inch]="1.25"
chromium_scale[1080p14inch]="1.25"

### <<< EDIT HERE


# Check if preset param is included in preset definitions
if ! array_contains "${presets[@]}" "$preset"; then
    error_exit "There's no preset called $preset. Try again."
fi

echo "Chosen preset: $preset"


# GNOME SETTINGS

# Font scaling
gsettings set org.gnome.desktop.interface text-scaling-factor ${gnome_font_scale[$preset]} \
    || error_exit "Error setting Gnome font scale. Exiting."
echo "Gnome font scale set to ${gnome_font_scale[$preset]}"

# Dash icons size
gsettings set org.gnome.shell.extensions.dash-to-dock dash-max-icon-size ${gnome_icon_size[$preset]} \
    || error_exit "Error setting Dash icon size. Exiting."
echo "Dash icon size set to ${gnome_icon_size[$preset]} px"

# Cursor size
gsettings set org.gnome.desktop.interface cursor-size ${gnome_cursor_size[$preset]} \
    || error_exit "Error setting Cursor size. Exiting."
echo "Cursor size set to ${gnome_cursor_size[$preset]} px"


# FIREFOX SETTINGS
if [[ ${firefox_profile_folder} == "" ]]; then
    echo "Warning: No Firefox preset folder given."
else
    cd "$HOME/.mozilla/firefox/$firefox_profile_folder/" \
        || error_exit "Error: There's no firefox config dir under $HOME/.mozilla/firefox/$firefox_profile_folder/. Exiting."
    # user.js can be missing.
    # FIXME: Single quotes vs. double quotes...
    if [[ -f "user.js" ]]; then
        grep -q "user_pref('layout.css.devPixelsPerPx'" user.js \
            && sed -i "s/.*user_pref('layout.css.devPixelsPerPx'.*/user_pref('layout.css.devPixelsPerPx', '${firefox_scale[$preset]}');/" user.js \
        || echo "user_pref('layout.css.devPixelsPerPx', '${firefox_scale[$preset]}');" >> user.js \
        || error_exit "Error: Cannot write to Firefox user.js in $HOME/.mozilla/firefox/$firefox_profile_folder/. Exiting."
    else
        echo "Firefox user.js created."
        echo "user_pref('layout.css.devPixelsPerPx', '${firefox_scale[$preset]}');" > user.js \
        || error_exit "Error: Cannot write to Firefox user.js in $HOME/.mozilla/firefox/$firefox_profile_folder/. Exiting."
    fi
    echo "Firefox pixels per px set to ${firefox_scale[$preset]} - Restart Firefox to see the effect"
fi


# CHROMIUM SNAP SETTINGS
sudo sed -i "s/\/snap\/bin\/chromium.*%U/\/snap\/bin\/chromium --force-device-scale-factor=${chromium_scale[$preset]} %U/" /var/lib/snapd/desktop/applications/chromium_chromium.desktop \
    || error_exit "Cannot set Chromium config to ${chromium_scale[$preset]}."
echo "Chromium zoom set to ${chromium_scale[$preset]} - Restart Chromium to see the effect"