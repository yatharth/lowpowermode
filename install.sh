#!/usr/bin/env bash
python3 setup_launchee.py py2app
python3 setup_launcher.py py2app
cp -r 'dist/Low Power Mode (Helper).app' 'dist/Low Power Mode.app/Contents/Resources/'
cp -r 'dist/Low Power Mode.app' /Applications/
