#!/usr/bin/python3

import json
import os
import platform
import sys
from pathlib import Path
import subprocess

version = '1.0.0'


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
        lines.append(new_line)
    else:
        with open(user_js_path, 'r') as user_js_file:
            lines = user_js_file.readlines()
        if len(lines) == 0:
            lines.append(new_line)
        else:
            for index, line in enumerate(lines):
                if line.startswith('user_pref'):
                    lines[index] = new_line

    with open(user_js_path, 'w+') as user_js_file:
        user_js_file.writelines(lines)
    print(f"Firefox scaling set to {firefox_settings['scale']}")


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
    envVars = os.environ.copy()

    if(
        platform.system() != 'Linux'
        or 'XDG_CURRENT_DESKTOP' not in envVars
        or (envVars['XDG_CURRENT_DESKTOP'] != 'Unity' and "GNOME" not in envVars['XDG_CURRENT_DESKTOP'])
    ):
        error('This program is only useful on Linux with Gnome desktop.')

    settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json')

    if not os.path.isfile(settings_path):
        error('Error: No settings.json found.')

    if len(sys.argv) < 2:
        error('Error: You did not specify a preset')

    chosen_preset = sys.argv[1]

    print(f"gnome-app-scaler v. {version}\n")

    with open(settings_path, 'r') as settings_file:
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

        print('\nRestart Firefox & Chromium to see the changes.')
