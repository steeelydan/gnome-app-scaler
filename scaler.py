#!/usr/bin/python3

import json
import os
import sys
from pathlib import Path


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
                        if 0 == os.system("gsettings set org.gnome.desktop.interface text-scaling-factor %s" % font_scale):
                            print("Gnome font scale set to %s" % font_scale)
                        else:
                            error("Error: Gnome font scale could not be set to %s" %
                                  font_scale)

                    if icon_size:
                        if 0 == os.system("gsettings set org.gnome.shell.extensions.dash-to-dock dash-max-icon-size %s" % icon_size):
                            print("Gnome icon size set to %s px" % icon_size)
                        else:
                            error("Error: Gnome icon size could not be set to %s" %
                                  icon_size)

                    if cursor_size:
                        if 0 == os.system("gsettings set org.gnome.desktop.interface cursor-size %s" % cursor_size):
                            print("Gnome cursor size set to %s px" %
                                  cursor_size)
                        else:
                            error("Error: Gnome cursor size could not be set to %s" %
                                  cursor_size)

                if app_name == 'firefox':
                    firefox_config = config['firefox']
                    firefox_profile_dir = "%s/.mozilla/firefox/%s/" % (
                        Path.home(), firefox_config['profile_folder'])
                    user_js_path = firefox_profile_dir + 'user.js'
                    firefox_settings = presets[chosen_preset]['firefox']

                    if not os.path.isfile(user_js_path):
                        user_js_raw = open(user_js_path, 'x')
                    else:
                        user_js_raw = open(user_js_path)
                        lines = user_js_raw.readlines()
                        for index, line in enumerate(lines):
                            if line.startswith('user_pref'):
                                lines[index] = "user_pref('layout.css.devPixelsPerPx', '%s');" % firefox_settings[
                                    'scale'] + '\n'
                        user_js_raw.writelines(lines)
                    user_js_raw.close()
                    print("Firefox scaling set to %s" %
                          firefox_settings['scale'])

            break
