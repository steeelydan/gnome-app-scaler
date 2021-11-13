#!/usr/bin/python3

import json
import os
import sys
from pathlib import Path
import subprocess


def error(message):
    print(message)
    sys.exit(1)


def apply_gnome(gnome_settings):
    font_scale = 'font_scale' in gnome_settings and gnome_settings['font_scale']
    icon_size = 'icon_size' in gnome_settings and gnome_settings['icon_size']
    cursor_size = 'cursor_size' in gnome_settings and gnome_settings['cursor_size']

    if font_scale:
        if 0 == os.system(f"gsettings set org.gnome.desktop.interface text-scaling-factor {font_scale}"):
            print(f"Gnome font scale set to {font_scale}")
        else:
            error(
                f"Error: Gnome font scale could not be set to {font_scale}")

    if icon_size:
        if 0 == os.system(f"gsettings set org.gnome.shell.extensions.dash-to-dock dash-max-icon-size {icon_size}"):
            print(f"Gnome icon size set to {icon_size} px")
        else:
            error(
                f"Error: Gnome icon size could not be set to {icon_size}")

    if cursor_size:
        if 0 == os.system(f"gsettings set org.gnome.desktop.interface cursor-size {cursor_size}"):
            print(f"Gnome cursor size set to {cursor_size} px")
        else:
            error(
                f"Error: Gnome cursor size could not be set to {cursor_size}")


def apply_firefox(firefox_settings, firefox_config):
    firefox_profile_dir = f"{Path.home()}/.mozilla/firefox/{firefox_config['profile_folder']}/"
    user_js_path = firefox_profile_dir + 'user.js'

    new_line = f"user_pref('layout.css.devPixelsPerPx', '{firefox_settings['scale']}');\n"

    lines = []

    if not os.path.isfile(user_js_path):
        user_js_raw = open(user_js_path, 'x')
        lines.append(new_line)
    else:
        user_js_raw = open(user_js_path, 'r')
        lines = user_js_raw.readlines()
        if len(lines) == 0:
            lines.append(new_line)
        else:
            for index, line in enumerate(lines):
                if line.startswith('user_pref'):
                    lines[index] = new_line
    user_js_raw.close()
    user_js_raw = open(user_js_path, 'w')
    user_js_raw.writelines(lines)
    print(
        f"Firefox scaling set to {firefox_settings['scale']}")


def apply_chromium(chromium_settings):
    chromium_path = '/var/lib/snapd/desktop/applications/chromium_chromium.desktop'
    chromium_result = subprocess.run(
        ['sudo', 'sed',  '-i', f"s/\/snap\/bin\/chromium.*%U/\/snap\/bin\/chromium --force-device-scale-factor={chromium_settings['scale']} %U/", '/var/lib/snapd/desktop/applications/chromium_chromium.desktop'])
    if chromium_result.returncode == 0:
        print(
            f"Chromium scaling set to {chromium_settings['scale']}")
    else:
        error(
            f"Error setting chromium scale in: {chromium_path}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        error('Error: You did not specify a preset')

    chosen_preset = sys.argv[1]

    with open('settings.json', 'r') as settings_file:
        settings_parsed = json.loads(settings_file.read())
        presets = settings_parsed['presets']
        config = settings_parsed['config']

        if chosen_preset not in presets:
            error('Error: Preset does not exist.')

        for app_name in presets[chosen_preset]:
            if app_name == 'gnome':
                apply_gnome(presets[chosen_preset]['gnome'])
            elif app_name == 'firefox':
                apply_firefox(firefox_settings=presets[chosen_preset]['firefox'],
                              firefox_config=config['firefox'])
            elif app_name == 'chromium':
                apply_chromium(presets[chosen_preset]['chromium'])
