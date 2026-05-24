"""
Installs/updates the required dependencies for developing the library.

This installs everything not available through pip/optional-dependencies.

- git `version 2.54.0`
- github.CLI `version 2.92.0`

Commands are ran in the ***systems shell***.

Make sure you have officially cloned this repository from the source
[https://github.com/cooldood155/mypytools](
    https://github.com/cooldood155/mypytools
), or verify that this file *(./scripts/dev_deps.py)* does what it says.

Exit Codes:

  - `0` — Successfully executed the script
  - `1` — A shell command exited with a code other than 0
  - `2` — A shell command took longer than 5 minutes to complete
"""
# Standard library imports
import platform
import re
import subprocess
import sys
from typing import Optional

GIT_MIN = '2.54.0'
GH_MIN  = '2.92.0'

def get_installed_version(command: str) -> Optional[tuple[int, ...]] | None:
    """
    Run `<command> --version` and extract the first X.Y.Z found in the output.

    Returns:
        A tuple like (2, 54, 0), or None if the command isn't available.
    """
    result = subprocess.run(
        f"{command} --version",
        shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    match = re.search(r'(\d+)\.(\d+)\.(\d+)', result.stdout)
    if not match:
        return None
    return tuple(int(x) for x in match.groups())

def meets_min_version(command: str, min_version: str) -> bool:
    """
    Return True if the installed version is >= min_version.
    
    Returns False if the command returned with code `0` or the output did not
    match what was expected.

    Args:
        command:
          The CLI command to check (e.g. 'git')
        min_version:
          Required minimum version (e.g. '2.54.0')
    """
    installed = get_installed_version(command)
    if installed is None:
        return False
    required = tuple(int(x) for x in min_version.split('.'))
    return installed >= required

def run_command(command: str) -> None:
    """
    This will attempt to run the provided command.

    The script will exit if:

    - A code other than `0` is returned
    - It takes longer than 5 minutes to complete the script

    Args:
        command (str):
          The command to run
    """
    try:
        subprocess.run(command, shell=True, check=True, timeout=300)
    except subprocess.CalledProcessError as e:
        print(
            f'\nError executing command: {command} — '
            f'returned a code other than 0\n{e}'
        )
        sys.exit(1)
    except subprocess.TimeoutExpired as e:
        print(
            f'\nError executing command: {command} — '
            f'took longer than 5 minutes\n{e}'
        )
        sys.exit(2)

def is_command_available(command: str) -> bool:
    """
    Attept to run the command with `--version` appended looking for any output.

    Args:
        command (str):
          The command to use when running `<command> --version`

    Returns:
        bool: True if the command returns with code `0` and has output.
    """
    return subprocess.run(
        f'{command} --version',
        shell=True, capture_output=True
    ).returncode == 0

def install_if_missing_windows(package_id, command, min_version):
    """
    Checks if the dep is missing or doesn't meet the min-version requirement.

    - Installs it if missing
    - Updates it if outdatted
    - Skips it if it already meets all requirements
    """
    if not get_installed_version(command):
        print(f'Installing {command}...')
        run_command(f'winget install --id {package_id} --exact')
    elif not meets_min_version(command, min_version):
        print(f'Upgrading {command} to >= {min_version}...')
        run_command(f'winget upgrade --id {package_id} --exact')
    else:
        print(f'{command} >= {min_version} is already installed, skipping.')

def install_if_missing_mac(package, command, min_version):
    """
    Checks if the dep is missing or doesn't meet the min-version requirement.

    - Installs it if missing
    - Updates it if outdatted
    - Skips it if it already meets all requirements
    """
    if not get_installed_version(command):
        print(f'Installing {command}...')
        run_command(f'brew install {package}')
    elif not meets_min_version(command, min_version):
        print(f'Upgrading {command} to >= {min_version}...')
        run_command(f'brew upgrade {package}')
    else:
        print(f'{command} >= {min_version} is already installed, skipping.')

def install_if_missing_linux_apt(package, command, min_version):
    """
    Checks if the dep is missing or doesn't meet the min-version requirement.

    - Installs it if missing
    - Updates it if outdatted
    - Skips it if it already meets all requirements
    """
    if not get_installed_version(command):
        print(f'Installing {command}...')
        _apt_install(package)
    elif not meets_min_version(command, min_version):
        print(f'Upgrading {command} to >= {min_version}...')
        _apt_install(package)
    else:
        print(f'{command} >= {min_version} is already installed, skipping.')

def _apt_install(package):
    'Shared apt install logic (used for both fresh installs and upgrades).'
    if package == 'gh':
        for cmd in [
            'sudo mkdir -p -m 755 /etc/apt/keyrings',
            'wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg'
              ' | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null',
            'sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg',
            'echo "deb [arch=$(dpkg --print-architecture)'
              ' signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg]'
              ' https://cli.github.com/packages stable main"'
              ' | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null',
            'sudo apt update',
            'sudo apt install gh -y',
        ]:
            run_command(cmd)
    else:
        run_command(f'sudo apt-get update && sudo apt-get install -y {package}')


def main():
    'Installs/updates all of the required dependencies for your system.'
    os_type = platform.system()
    print(f'Detected OS: {os_type}')

    if os_type == 'Windows':
        install_if_missing_windows('Git.Git', 'git', GIT_MIN)
        install_if_missing_windows('GitHub.CLI', 'gh', GH_MIN)

    elif os_type == 'Darwin':
        install_if_missing_mac('git', 'git',GIT_MIN)
        install_if_missing_mac('gh', 'gh', GH_MIN)

    elif os_type == 'Linux':
        apt_available = subprocess.run(
            'type apt-get', shell=True, capture_output=True
        ).returncode == 0

        if apt_available:
            print('Detected Debian/Ubuntu system.')
            install_if_missing_linux_apt('git', 'git', GIT_MIN)
            install_if_missing_linux_apt('gh', 'gh', GH_MIN)
        else:
            print('Detected Fedora/RHEL system.')
            if not meets_min_version('git', GIT_MIN):
                run_command('sudo dnf install git -y')
            if not meets_min_version('gh', GIT_MIN):
                run_command(
                    'sudo dnf config-manager --add-repo '
                    'https://cli.github.com/packages/rpm/gh-cli.repo'
                )
                run_command('sudo dnf install gh -y')

    else:
        print(f'Unsupported OS: {os_type}')
        sys.exit(1)

    print('Installation complete!')


if __name__ == '__main__':
    main()