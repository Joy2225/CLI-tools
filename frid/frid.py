import sys
import os
import time
import subprocess

def check_avd_exists(avd_name):
    avd_path = f"C:\\Users\\{os.getlogin()}\\.android\\avd\\{avd_name}.avd"
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

def launch_shell_command(serial):
    cmd = f'start cmd /k "adb -s {serial} shell /data/local/tmp/frida-server"'
    subprocess.Popen(cmd, shell=True)

def adb_root(target_serial):
    check_root = os.popen(f"adb -s {target_serial} root").read().strip()
    if check_root.startswith("adbd cannot run as root in production builds"):
        print("Failed to restart ADB as root.")
        return False
    return True


def main():
    print("Welcome to Frida AVD Launcher!")
    print("This script will start an AVD and run Frida server on it.")
    avd = sys.argv[1].strip()
    if not avd:
        print("Usage: frid <avd_name>")
        sys.exit(1)

    if not check_avd_exists(avd):
        print(f"AVD '{avd}' does not exist.")
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

    launch_shell_command(target_serial)

if __name__ == "__main__":
    main()