import sys
import os
import time
import subprocess
import platform
from shutil import which
import argparse

def check_os(avd):
    os_name = platform.system()
    if os_name == "Windows":
        return 0
    elif os_name == "Linux":
        return 1
    else:
        print(f"Operating System: {os_name} (Unrecognized or other OS)")
        return 2

def check_avd_exists_windows(avd_name):
    avd_path = f"C:\\Users\\{os.getlogin()}\\.android\\avd\\{avd_name}.avd"
    return os.path.exists(avd_path)

def check_avd_exists_linux(avd_name):
    avd_path = f"/home/{os.getlogin()}/.android/avd/{avd_name}.ini"
    return os.path.exists(avd_path)

def get_running_avd_serials():
    output = os.popen("adb devices").read().strip().split("\n")
    return [line.split()[0] for line in output if line and len(line.split()) > 1 and line.split()[1] == "device"]

def get_avd_name_from_serial(serial):
    return os.popen(f"adb -s {serial} emu avd name").read().strip().split("\n")[0]

def start_avd(avd_name):
    print(f"Starting AVD '{avd_name}'...")
    subprocess.Popen(f"emulator -avd {avd_name}", shell=True)
    # Wait until it's up and adb is ready
    print("Waiting for device to boot...")
    while True:
        serials = get_running_avd_serials()
        for s in serials:
            name = get_avd_name_from_serial(s)
            print(f"Checking AVD name for serial {s}: {name}")
            if name == avd_name:
                # Wait for the device to be fully booted
                boot_status = os.popen(f"adb -s {s} shell getprop sys.boot_completed").read().strip()
                if boot_status == "1":
                    return s
        time.sleep(2)

def launch_shell_command_windows(serial):
    cmd = f'start cmd /k "adb -s {serial} shell /data/local/tmp/frida-server"'
    subprocess.Popen(cmd, shell=True)

def launch_shell_command_linux(serial, preferred="kitty"):
    terminals = {
        "gnome-terminal": ["--", "adb", "-s", serial, "shell", "/data/local/tmp/frida-server"],
        "konsole": ["-e", "adb", "-s", serial, "shell", "/data/local/tmp/frida-server"],
        "xfce4-terminal": ["--command", f"adb -s {serial} shell /data/local/tmp/frida-server"],
        "xterm": ["-hold", "-e", "adb", "-s", serial, "shell", "/data/local/tmp/frida-server"],
        "kitty": ["--detach", "bash", "-c", f"adb -s {serial} shell /data/local/tmp/frida-server; exec bash"]
    }

    if preferred in terminals and which(preferred):
        print(f"Launching in preferred terminal: {preferred}")
        subprocess.Popen([preferred] + terminals[preferred])
        return

    # Fallback
    for term, args in terminals.items():
        if which(term):
            print(f"Preferred terminal not found. Falling back to: {term}")
            subprocess.Popen([term] + args)
            return

    print("No supported terminal found. Running command without terminal.")
    subprocess.Popen(["adb", "-s", serial, "shell", "/data/local/tmp/frida-server"])

def adb_root(target_serial):
    check_root = os.popen(f"adb -s {target_serial} root").read().strip()
    if check_root.startswith("adbd cannot run as root in production builds"):
        print("Failed to restart ADB as root.")
        return False
    return True


def main():

    parser = argparse.ArgumentParser(description="Frida AVD Launcher")
    parser.add_argument("avd", help="Name of the AVD to launch")
    parser.add_argument("--term", help="Preferred terminal emulator (e.g. kitty, gnome-terminal, xterm)", default="kitty")

    args = parser.parse_args()
    avd = args.avd.strip()
    preferred_terminal = args.term.strip()

    print("Welcome to Frida AVD Launcher!!")
    print("This script will start an AVD and run Frida server on it")

    os_check = check_os(avd)
    if os_check == 2:
        print("Unsupported operating system. Please use Windows or Linux.")
        sys.exit(1)
    elif os_check == 0:
        if not check_avd_exists_windows(avd):
            print(f"AVD '{avd}' does not exist.")
            sys.exit(1)
    elif os_check == 1:
        if not check_avd_exists_linux(avd):
            print(f"AVD '{avd}' does not exist.")
            sys.exit(1)
    else:
        print("Error checking AVD existence.")
        sys.exit(1)

    serials = get_running_avd_serials()
    target_serial = None
    for serial in serials:
        name = get_avd_name_from_serial(serial)
        if name == avd:
            target_serial = serial
            print(f"AVD '{avd}' is already running.")
            break

    if not target_serial:
        target_serial = start_avd(avd)

    print(f"AVD '{avd}' is running with serial {target_serial}.")

    if not adb_root(target_serial):
        sys.exit(1)

    print("ADB is now running as root.")

    if os_check == 0:
        launch_shell_command_windows(target_serial)
    elif os_check == 1:
        launch_shell_command_linux(target_serial, preferred_terminal)
    else:
        print("Unsupported operating system for launching shell command.")
        sys.exit(1)

if __name__ == "__main__":
    main()