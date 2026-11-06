import subprocess

class AdbDevice:
    def __init__(self, serial):
        self.serial = serial

    def run(self, command):
        cmd = ["adb", "-s", self.serial] + command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        return result.stdout

    def shell(self, command):
        return self.run(["shell"] + command.split())

    def verify_device(serial):
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        if serial not in result.stdout:
            raise RuntimeError(
                f"Device {serial} not found. "
                "Did you run 'adb-set <device_name>'?"
            )
