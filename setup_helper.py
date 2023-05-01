from setuptools import setup

def setup_helper(*, python_script: str, app_name: str) -> None:

    OPTIONS = {
        'iconfile': 'icon.icns',
        'plist': {
            # This hides the app from the dock and app switcher.
            'LSUIElement': '1',
            # CFBundleName is the short name, and CFBundleDisplayName is the longer name.
            'CFBundleName': app_name,
            'CFBundleDisplayName': app_name,
            # Some options I did not end up needing:
            #
            #   'NSHighResolutionCapable': True,
            #   'NSAppleScriptEnabled': True,

        },
    }

    setup(
        app=[python_script],
        data_files=[],
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )
