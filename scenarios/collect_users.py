from pathlib import Path

from core.adb import AdbDevice
from core.utils import write_file


def collect_users(
        device: AdbDevice,
        output_dir: Path):

    print("[INFO] Collecting user information...")

    commands = {
        "current_user.txt":
            "am get-current-user",

        "users_list.txt":
            "pm list users",

        "dumpsys_user.txt":
            "dumpsys user",

        "dcsm_services.txt":
            "dumpsys activity services com.harman.DCSM"
    }

    for filename, command in commands.items():

        print(f"[INFO] {filename}")

        result = device.shell(command)

        write_file(
            output_dir,
            filename,
            result
        )

    print("[INFO] User collection completed.")