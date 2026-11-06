from pathlib import Path

from core.adb import AdbDevice
from core.utils import write_file


def collect_build_info(device: AdbDevice, output_dir: Path) -> None:
    """Save Android build properties from a device into separate text files."""
    commands = {
        "build_id.txt": "getprop ro.build.id",
        "display_id.txt": "getprop ro.build.display.id",
        "incremental.txt": "getprop ro.build.version.incremental",
        "sdk.txt": "getprop ro.build.version.sdk",
    }
    for filename, command in commands.items():
        write_file(output_dir, filename, device.shell(command))
        print(f"[INFO] {filename}")
