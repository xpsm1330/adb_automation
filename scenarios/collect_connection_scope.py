from pathlib import Path
from datetime import datetime

from core.adb import AdbDevice
from core.utils import write_file


def collect_connection_scope(
        device: AdbDevice,
        output_dir: Path,
        phase: str):

    print(f"[INFO] Collecting connection scope ({phase})")

    unix_time = device.shell("date +%s")
    human_time = device.shell("date")

    write_file(
        output_dir,
        f"{phase}_time.txt",
        human_time
    )

    write_file(
        output_dir,
        f"{phase}_epoch.txt",
        unix_time
    )

    commands = {
        f"{phase}_current_user.txt":
            "am get-current-user",

        f"{phase}_users.txt":
            "pm list users",

        f"{phase}_dcsm.txt":
            "dumpsys activity services com.harman.DCSM",

        f"{phase}_activity.txt":
            "dumpsys activity",

        f"{phase}_package_com_harman.txt":
            "pm list packages | grep harman",

        f"{phase}_device_config.txt":
            "device_config list"
    }

    for filename, command in commands.items():

        print(f"[INFO] {filename}")

        result = device.shell(command)

        write_file(
            output_dir,
            filename,
            result)

    print(
        f"[INFO] Connection scope collection ({phase}) completed."
    )