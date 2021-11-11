#!/usr/bin/python3

import json
import os
import sys


def error(message):
    print(message)
    sys.exit(1)


if len(sys.argv) < 2:
    error('Error: You did not specify a preset')

settings_file = open('settings.json')
settings = json.loads(settings_file.read())

chosen_preset = sys.argv[1]

if not chosen_preset in settings:
    error('Error: Preset does not exist.')

for preset_name in settings:
    if chosen_preset == preset_name:
        for app_name in settings[preset_name]:
            if app_name == 'gnome':
                gnome_settings = settings[chosen_preset]['gnome']

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
                        print("Gnome cursor size set to %s px" % cursor_size)
                    else:
                        error("Error: Gnome cursor size could not be set to %s" %
                              cursor_size)
        break
