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
    if '"' in command:
        panic("Escaping double quotes is not supported yet.")
    output_bytes = subprocess.check_output(
        ["osascript", "-e", f"do shell script \"{command}\" with administrator privileges"])
    output = output_bytes.decode().strip()
    log_command(command, output)
    return output


# The launcher expects the launchee's .app bundle to be inside the
#  "Resources" folder of the launcher's .app bundle.
PATH_TO_LAUNCHEE = '.'
LAUNCHEE_APP_NAME = 'Low Power Mode (Helper)'


def launch() -> None:
    shell_with_password_prompt(f"sudo '{PATH_TO_LAUNCHEE}/{LAUNCHEE_APP_NAME}.app/Contents/MacOS/{LAUNCHEE_APP_NAME}'")


if __name__ == "__main__":
    launch()
