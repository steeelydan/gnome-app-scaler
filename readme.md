# GNOME App Scaler

An alternative to native GNOME UI scaling. Specify different scaling values per app.

Useful when alternating between a laptop screen and an external screen with different dpi or resolution.

Includes presets for

-   Gnome Desktop (font size, dock icons, cursor)
-   Firefox
-   Chromium
-   VSCode

Of course, you're free to extend the script according to your needs.

## Usage

`./scaler.sh mode`

Default mode presets:

-   `default`
-   `1080p14inch` (Thinkpads,etc.)

### Permissions & Privileges

Configure the appropriate execution permissions for `scaler.sh`.
Unfortunately, Chromium .desktop file manipulation needs root privileges.

### Make your own preset

-   Add your preset by extending the `presets` array
-   Specify your preset's scale values below

### Aliasing

When aliasing, execute via `bash` because `sh` does not support arrays.
Example:

`alias dpireset='/bin/bash /home/willy/scripts/scaler.sh default'`

## To Do

-   Rewrite it in Python :)
-   Interactive config: E.g. ask for Firefox user string once, save it
