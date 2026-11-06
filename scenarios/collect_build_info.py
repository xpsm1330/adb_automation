from core.adb import AdbDevice
from core.logger import save_log

device = AdbDevice("6b93ec37")

commands = {
    "build_id.txt":
        "getprop ro.build.id",

    "display_id.txt":
        "getprop ro.build.display.id",

    "incremental.txt":
        "getprop ro.build.version.incremental",

    "sdk.txt":
        "getprop ro.build.version.sdk"
}

for filename, cmd in commands.items():

    content = device.shell(cmd)

    save_log(
        "logs/build_info",
        filename,
        content
    )