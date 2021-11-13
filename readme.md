# GNOME App Scaler

An alternative to native GNOME UI scaling. Specify different scaling values per app.

Useful when alternating between a laptop screen and an external screen with different dpi or resolution.

Includes presets for

-   Gnome Desktop (font size, dock icons, cursor)
-   Firefox
-   Chromium

Of course, you're free to extend the script according to your needs.

## Requirements

Python 3

## Usage

-   Enter your Firefox profile directory in `settings.json`
-   Edit `settings.json` as desired or add presets
-   `./scaler.py <PRESET>`

Default presets:

-   `default`
-   `1080p14inch` (Thinkpads,etc.)
-   `4k32inch` (large 4k monitors)

### Permissions & Privileges

Unfortunately, Chromium `.desktop` file manipulation needs root privileges. The scaler starts a root subprocess & asks you for your password when the time has come.

### Aliasing

Example:

```bash
alias dpireset='/home/willy/scripts/scaler.py default'
alias dpilaptop='/home/willy/scripts/scaler.py 1080p14inch'
```
