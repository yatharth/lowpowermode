# Low Power Mode

Simple macOS menu bar widget to let you toggle Low Power Mode on and off.

## Motivation

macOS ships with a "Low Power Mode", but strangely, there is no menu bar widget for it, nor any way to make it show up in Control Centre.

## Installation

Just close the repo and run `./install.sh`. You'll find a "Low Power Mode" app has been installed to your /Applications folder. 


## Technical Design

It is tricky to run commands with sudo in a macOS app without prompting the user for their password every time.

Turning Low Power Mode on and off requires sudo access. To avoid reprompting the user for their password every time, there is a helper application that is launched in a special sudo way by the main application. That way the main application only needs to ask the user for their password once.

Most other approaches involved something insecure, ugly, or complicated. For example:

- You could edit your sudoers file to allow anyone to call the `pmset` command with sudo without needing a password, but that is insecure, and plus, now installing the app cannot be automated but rather requires someone to use visudo. 
- You could just run a Python GUI script from the terminal (something like `sudo launchee.py`) without bundling it into a macOS app, but that clutters the dock and app switcher with an ugly app icon. 
- You could create a privileged helper service the app communicates with, but that gets very complicated for such a simple app.


## TODO

- [ ] Share the code for running shell commands between `launchee.py` and `launcher.py` without it breaking the `py2app` build process.
- [ ] Use the `logging` library to redirect standard output to a logging file, instead of having the `log_string()` function.

 
