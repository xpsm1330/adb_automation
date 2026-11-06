import subprocess


class AdbDevice:
    def __init__(self, serial: str):
        self.serial = serial

    def run(self, command: list[str]) -> str:
        cmd = ["adb", "-s", self.serial, *command]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            details = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(
                f"ADB command failed for device {self.serial}: {details}"
            )
        return result.stdout

    def shell(self, command: str) -> str:
        # Pass one command string so Android's shell can interpret quoting and pipes.
        return self.run(["shell", command])

    @staticmethod
    def verify_device(serial: str) -> None:
        result = subprocess.run(
            ["adb", "devices"], capture_output=True, text=True, check=True
        )
        for line in result.stdout.splitlines()[1:]:
            fields = line.split()
            if fields and fields[0] == serial:
                if len(fields) > 1 and fields[1] == "device":
                    return
                state = fields[1] if len(fields) > 1 else "unknown"
                raise RuntimeError(f"Device {serial} is not ready (state: {state}).")

        raise RuntimeError(
            f"Device {serial} not found. Connect it and authorize ADB debugging."
        )
