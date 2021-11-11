import json

settings_file = open('settings.json')
settings = json.loads(settings_file.read())

print(settings)
