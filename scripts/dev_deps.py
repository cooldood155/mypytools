"""
Installs/updates the required dependencies for developing the library.

This installs everything not available through pip/optional-dependencies.

- git `version 2.54.0`
- github.CLI `version 2.92.0`
- C++ compiler with C++17 support

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
import shutil
import subprocess
import sys

GIT_MIN = '2.54.0'
GH_MIN = '2.92.0'
CXX_STANDARD = 17


# ——{ Helpers }————————————————————————————————————————————————————————————————


def run_command(command: str) -> None:
    """
    Run a shell command, exiting the script on failure or timeout.

    The script will exit if:

    - A code other than ``0`` is returned
    - It takes longer than 5 minutes to complete

    Args:
        command: The shell command to run.
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


def get_installed_version(command: str) -> tuple[int, ...] | None:
    """
    Run ``<command> --version`` and extract the first X.Y.Z found in output.

    Args:
        command: The CLI command to query (e.g. ``'git'``).

    Returns:
        A version tuple like ``(2, 54, 0)``, or ``None`` if unavailable.
    """
    result = subprocess.run(
        f'{command} --version', shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    match = re.search(r'(\d+)\.(\d+)\.(\d+)', result.stdout)
    if not match:
        return None
    return tuple(int(x) for x in match.groups())


def meets_min_version(command: str, min_version: str) -> bool:
    """
    Return ``True`` if the installed version of a command is >= min_version.

    Args:
        command: The CLI command to check (e.g. ``'git'``).
        min_version: Required minimum version string (e.g. ``'2.54.0'``).

    Returns:
        ``False`` if the command is unavailable or below the minimum.
    """
    installed = get_installed_version(command)
    if installed is None:
        return False
    required = tuple(int(x) for x in min_version.split('.'))
    return installed >= required


def apt_available() -> bool:
    """Return ``True`` if apt-get is available on this system."""
    return (
        subprocess.run(
            'type apt-get', shell=True, capture_output=True
        ).returncode
        == 0
    )


# ——{ Compiler }———————————————————————————————————————————————————————————————


def _compiler_supports_cxx17(executable: str) -> bool:
    """
    Compile a trivial C++17 snippet to confirm the compiler supports it.

    Args:
        executable: The compiler binary to test (e.g. ``'g++'``, ``'cl'``).

    Returns:
        ``True`` if the compiler is present and accepts ``-std=c++17``
        (or ``/std:c++17`` for MSVC).
    """
    if not shutil.which(executable):
        return False
    snippet = 'int main(){if constexpr(true){} return 0;}'
    if executable == 'cl':
        command = 'cl /std:c++17 /EHsc /nologo - /Fe:nul'
    else:
        command = f'{executable} -std=c++17 -x c++ - -o /dev/null'
    result = subprocess.run(
        command,
        input=snippet,
        shell=True,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _find_cxx17_compiler(os_type: str) -> str | None:
    """
    Return the first C++17-capable compiler found for this platform, or None.

    Args:
        os_type: The platform string (``'Windows'``, ``'Darwin'``, ``'Linux'``).
    """
    candidates: dict[str, list[str]] = {
        'Windows': ['cl'],
        'Darwin': ['clang++', 'g++'],
        'Linux': ['g++', 'clang++'],
    }
    for compiler in candidates.get(os_type, ['g++', 'clang++']):
        if _compiler_supports_cxx17(compiler):
            return compiler
    return None


def check_compiler(os_type: str) -> None:
    """
    Verify a C++17-capable compiler is present; install or guide if not.

    Auto-installs on Linux (apt/dnf). Prints manual instructions for
    Windows and macOS, then exits with code ``1`` if no compiler is found
    after the attempt.

    Args:
        os_type: The platform string (``'Windows'``, ``'Darwin'``, ``'Linux'``).
    """
    print('Checking for a C++17-capable compiler...')

    compiler = _find_cxx17_compiler(os_type)
    if compiler:
        print(f'Found compatible compiler: {compiler}, skipping.')
        return

    print(f'No C++{CXX_STANDARD}-capable compiler found.')

    if os_type == 'Windows':
        print(
            '\nInstall MSVC manually:\n'
            '  1. Download Visual Studio Build Tools:\n'
            '     https://visualstudio.microsoft.com/visual-cpp-build-tools/\n'
            '  2. Select the "Desktop development with C++" workload.\n'
            '  3. Re-run this script once installation is complete.'
        )
        sys.exit(1)

    elif os_type == 'Darwin':
        print('Installing Xcode Command Line Tools (may open a GUI prompt)...')
        run_command('xcode-select --install')
        if not _find_cxx17_compiler(os_type):
            print(
                '\nCompiler not yet available — if a GUI installer opened, '
                'complete it and re-run this script.'
            )
            sys.exit(1)

    elif os_type == 'Linux':
        if apt_available():
            print('Installing build-essential (gcc/g++)...')
            run_command(
                'sudo apt-get update && '
                'sudo apt-get install -y build-essential'
            )
        else:
            print('Installing gcc-c++ via dnf...')
            run_command('sudo dnf install gcc-c++ -y')
        if not _find_cxx17_compiler(os_type):
            print(
                'Compiler installation succeeded but no C++17 compiler found.'
            )
            sys.exit(1)


# ——{ Dependencies }———————————————————————————————————————————————————————————


def _install_dep(
    command: str,
    min_version: str,
    install_cmd: str,
    upgrade_cmd: str,
) -> None:
    """
    Install or upgrade a CLI dependency to meet a minimum version requirement.

    - Installs if missing.
    - Upgrades if below ``min_version``.
    - Skips if already satisfied.

    Args:
        command: The CLI command to check (e.g. ``'git'``).
        min_version: Required minimum version string (e.g. ``'2.54.0'``).
        install_cmd: Shell command to run for a fresh install.
        upgrade_cmd: Shell command to run for an upgrade.
    """
    if get_installed_version(command) is None:
        print(f'Installing {command}...')
        run_command(install_cmd)
    elif not meets_min_version(command, min_version):
        print(f'Upgrading {command} to >= {min_version}...')
        run_command(upgrade_cmd)
    else:
        print(f'{command} >= {min_version} already installed, skipping.')


def _apt_install(package: str) -> None:
    """
    Install a package via apt, using the GitHub CLI keyring flow for ``gh``.

    Args:
        package: The apt package name to install (e.g. ``'git'``, ``'gh'``).
    """
    if package == 'gh':
        for cmd in [
            'sudo mkdir -p -m 755 /etc/apt/keyrings',
            'wget -qO-'
            ' https://cli.github.com/packages/githubcli-archive-keyring.gpg'
            ' | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg'
            ' > /dev/null',
            'sudo chmod go+r'
            ' /etc/apt/keyrings/githubcli-archive-keyring.gpg',
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


# ——{ Main }———————————————————————————————————————————————————————————————————


def main() -> None:
    """Installs/updates all of the required dependencies for your system."""
    os_type = platform.system()
    print(f'Detected OS: {os_type}')

    check_compiler(os_type)

    if os_type == 'Windows':
        _install_dep(
            'git',
            GIT_MIN,
            install_cmd='winget install --id Git.Git --exact',
            upgrade_cmd='winget upgrade --id Git.Git --exact',
        )
        _install_dep(
            'gh',
            GH_MIN,
            install_cmd='winget install --id GitHub.CLI --exact',
            upgrade_cmd='winget upgrade --id GitHub.CLI --exact',
        )

    elif os_type == 'Darwin':
        _install_dep(
            'git',
            GIT_MIN,
            install_cmd='brew install git',
            upgrade_cmd='brew upgrade git',
        )
        _install_dep(
            'gh',
            GH_MIN,
            install_cmd='brew install gh',
            upgrade_cmd='brew upgrade gh',
        )

    elif os_type == 'Linux':
        if apt_available():
            print('Detected Debian/Ubuntu system.')
            _install_dep(
                'git',
                GIT_MIN,
                install_cmd=(
                    'sudo apt-get update && sudo apt-get install -y git'
                ),
                upgrade_cmd=(
                    'sudo apt-get update && sudo apt-get install -y git'
                ),
            )
            if not meets_min_version('gh', GH_MIN):
                _apt_install('gh')
            else:
                print(f'gh >= {GH_MIN} already installed, skipping.')
        else:
            print('Detected Fedora/RHEL system.')
            if not meets_min_version('git', GIT_MIN):
                run_command('sudo dnf install git -y')
            else:
                print(f'git >= {GIT_MIN} already installed, skipping.')

            if not meets_min_version('gh', GH_MIN):
                if get_installed_version('gh') is None:
                    run_command(
                        'sudo dnf config-manager --add-repo '
                        'https://cli.github.com/packages/rpm/gh-cli.repo'
                    )
                run_command('sudo dnf install gh -y')
            else:
                print(f'gh >= {GH_MIN} already installed, skipping.')

    else:
        print(f'Unsupported OS: {os_type}')
        sys.exit(1)

    print('Installation complete!')


if __name__ == '__main__':
    main()
