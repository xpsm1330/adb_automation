# import subprocess

# class AdbDevice:
#     def __init__(self, serial):
#         self.serial = serial

#     def run(self, command):
#         cmd = ["adb", "-s", self.serial] + command
#         result = subprocess.run(
#             cmd,
#             capture_output=True,
#             text=True
#         )

#         return result.stdout

#     def shell(self, command):
#         return self.run(["shell"] + command.split())

from pathlib import Path
from subprocess import Popen


class LogcatLogger:

    def __init__(self, device_id: str, output_file: Path):
        self.device_id = device_id
        self.output_file = output_file
        self.process = None

    def clear(self):
        import subprocess

        subprocess.run(
            ["adb", "-s", self.device_id, "logcat", "-c"],
            check=False
        )

    def start(self):

        f = open(
            self.output_file,
            "w",
            encoding="utf-8",
            buffering=1
        )

        self.process = Popen(
            [
                "adb",
                "-s",
                self.device_id,
                "logcat",
                "-v",
                "threadtime"
            ],
            stdout=f,
            stderr=f,
            text=True
        )

        return self.process

    def stop(self):
        if self.process:
            self.process.terminate()