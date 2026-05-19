import platform
import subprocess
import sys


def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}\n{e}")
        sys.exit(1)


def is_command_available(command):
    return subprocess.run(
        f"{command} --version",
        shell=True, capture_output=True
    ).returncode == 0


def install_if_missing_windows(package_id, command):
    if is_command_available(command):
        print(f"{command} is already installed, skipping.")
    else:
        print(f"Installing {command}...")
        run_command(f"winget install --id {package_id} --exact")


def install_if_missing_mac(package, command):
    if is_command_available(command):
        print(f"{command} is already installed, skipping.")
    else:
        print(f"Installing {command}...")
        run_command(f"brew install {package}")


def install_if_missing_linux_apt(package, command):
    if is_command_available(command):
        print(f"{command} is already installed, skipping.")
        return
    print(f"Installing {command}...")
    if package == "gh":
        for cmd in [
            "sudo mkdir -p -m 755 /etc/apt/keyrings",
            "wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null",
            "sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg",
            'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null',
            "sudo apt update",
            "sudo apt install gh -y",
        ]:
            run_command(cmd)
    else:
        run_command(f"sudo apt-get update && sudo apt-get install -y {package}")


def main():
    os_type = platform.system()
    print(f"Detected OS: {os_type}")

    if os_type == "Windows":
        install_if_missing_windows("Git.Git", "git")
        install_if_missing_windows("GitHub.CLI", "gh")

    elif os_type == "Darwin":
        install_if_missing_mac("git", "git")
        install_if_missing_mac("gh", "gh")

    elif os_type == "Linux":
        apt_available = subprocess.run(
            "type apt-get", shell=True, capture_output=True
        ).returncode == 0

        if apt_available:
            print("Detected Debian/Ubuntu system.")
            install_if_missing_linux_apt("git", "git")
            install_if_missing_linux_apt("gh", "gh")
        else:
            print("Detected Fedora/RHEL system.")
            if not is_command_available("git"):
                run_command("sudo dnf install git -y")
            if not is_command_available("gh"):
                run_command("sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo")
                run_command("sudo dnf install gh -y")

    else:
        print(f"Unsupported OS: {os_type}")
        sys.exit(1)

    print("Installation complete!")


if __name__ == "__main__":
    main()