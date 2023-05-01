import inspect
import os
import subprocess


def dedent(string: str) -> str:
    return inspect.cleandoc(string)


def log_string(string: str, /) -> None:
    with open('/tmp/lowpowermode.txt', 'a') as f:
        f.write(string)


def log_command(command: str, output: str, /) -> None:
    log_string(dedent(f"""
        > {command}
        {output}
        ===
    """))


def panic(message: str, /) -> None:
    log_string(message)
    raise RuntimeError(message)


def shell(command: str, /) -> str:
    # The "2>&1" redirects stderr to stdout, in case we need it.
    output = os.popen(f"{command} 2>&1").read().strip()
    log_command(command, output)
    return output


def shell_with_password_prompt(command: str, /) -> str:
    if '"' in command or "'" in command:
        panic("Escaping is not supported yet.")
    output_bytes = subprocess.check_output(
        ["osascript", "-e", f"do shell script \"{command}\" with administrator privileges"])
    output = output_bytes.decode().strip()
    log_command(command, output)
    return output


import rumps


def is_lowpowermode_on() -> bool | None:
    output = shell('sudo pmset -g | grep lowpowermode | tail -c 2')
    match output:
        case "0":
            return False
        case "1":
            return True
        case _:
            return None


def enable_lowpowermode() -> None:
    shell("sudo pmset -a lowpowermode 1")


def disable_lowpowermode() -> None:
    shell("sudo pmset -a lowpowermode 0")


def toggle_lowpowermode():
    if is_lowpowermode_on():
        disable_lowpowermode()
    else:
        enable_lowpowermode()


APP_NAME = "Low Power Mode"
TITLE_WHEN_OFF = "🔋"
TITLE_WHEN_ON = "🪫"
TITLE_WHEN_ERROR = "🥴"
TOGGLE_BUTTON = "Toggle Low Power Mode"
ENABLE_BUTTON = "Enable"
DISABLE_BUTTON = "Disable"


class LowPowerModeStatusBar(rumps.App):
    def __init__(self):
        super().__init__(APP_NAME)
        self.menu = [TOGGLE_BUTTON, ENABLE_BUTTON, DISABLE_BUTTON]
        self.update_status()

    @rumps.clicked(TOGGLE_BUTTON)
    def toggle_low_power_mode(self, _):
        toggle_lowpowermode()
        self.update_status()

    @rumps.clicked(ENABLE_BUTTON)
    def enable_low_power_mode(self, _):
        enable_lowpowermode()
        self.update_status()

    @rumps.clicked(DISABLE_BUTTON)
    def disable_low_power_mode(self, _):
        disable_lowpowermode()
        self.update_status()

    def update_status(self):
        match is_lowpowermode_on():
            case True:
                self.title = TITLE_WHEN_ON
            case False:
                self.title = TITLE_WHEN_OFF
            case _:
                self.title = TITLE_WHEN_ERROR


if __name__ == "__main__":
    LowPowerModeStatusBar().run()
