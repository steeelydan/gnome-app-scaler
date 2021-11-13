#!/usr/bin/python3

import json
import os
import sys
from pathlib import Path
import subprocess


def error(message):
    print(message)
    sys.exit(1)


if len(sys.argv) < 2:
    error('Error: You did not specify a preset')


with open('settings.json', 'r') as settings_file:
    settings_parsed = json.loads(settings_file.read())
    presets = settings_parsed['presets']
    config = settings_parsed['config']

    chosen_preset = sys.argv[1]

    if not chosen_preset in presets:
        error('Error: Preset does not exist.')

    for preset_name in presets:
        if chosen_preset == preset_name:
            for app_name in presets[preset_name]:
                if app_name == 'gnome':
                    gnome_settings = presets[chosen_preset]['gnome']

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

                if app_name == 'firefox':
                    firefox_config = config['firefox']
                    firefox_profile_dir = f"{Path.home()}/.mozilla/firefox/{firefox_config['profile_folder']}/"
                    user_js_path = firefox_profile_dir + 'user.js'
                    firefox_settings = presets[chosen_preset]['firefox']

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

                if app_name == 'chromium':
                    chromium_path = '/var/lib/snapd/desktop/applications/chromium_chromium.desktop'
                    chromium_settings = presets[chosen_preset]['chromium']
                    subprocess.run(
                        ['sudo', 'sed',  '-i', f"s/\/snap\/bin\/chromium.*%U/\/snap\/bin\/chromium --force-device-scale-factor={chromium_settings['scale']} %U/", '/var/lib/snapd/desktop/applications/chromium_chromium.desktop'])
                    print(f"Chromium scaling set to {chromium_settings['scale']}")

                    # with open(chromium_path) as chromium_config:
                    #     lines = chromium_config.readlines()
                    #     for index, line in enumerate(lines):
                    #         if (line.startswith('Exec=env BAMF_DESKTOP_FILE_HINT=/var/lib/snapd/desktop/applications/chromium_chromium.desktop /snap/bin/chromium')):
                    #             lines[
                    #                 index] = f"Exec=env BAMF_DESKTOP_FILE_HINT=/var/lib/snapd/desktop/applications/chromium_chromium.desktop /snap/bin/chromium --force-device-scale-factor={chromium_settings['scale']} %U\n"
                    #     print(chromium_config.read())
                    #     chromium_config.writelines(lines)

            break
