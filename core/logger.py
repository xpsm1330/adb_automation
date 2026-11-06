from pathlib import Path
import subprocess


class LogcatLogger:
    def __init__(self, device_id: str, output_file: Path):
        self.device_id = device_id
        self.output_file = output_file
        self.process: subprocess.Popen | None = None
        self._log_file = None

    def clear(self) -> None:
        subprocess.run(
            ["adb", "-s", self.device_id, "logcat", "-c"],
            check=True,
            capture_output=True,
            text=True,
        )

    def start(self) -> subprocess.Popen:
        if self.process is not None and self.process.poll() is None:
            raise RuntimeError(f"Logcat is already running for {self.device_id}.")

        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self._log_file = self.output_file.open(
            "w", encoding="utf-8", buffering=1
        )
        try:
            self.process = subprocess.Popen(
                ["adb", "-s", self.device_id, "logcat", "-v", "threadtime"],
                stdout=self._log_file,
                stderr=subprocess.STDOUT,
                text=True,
            )
        except Exception:
            self._log_file.close()
            self._log_file = None
            raise
        return self.process

    def stop(self) -> None:
        if self.process is not None:
            if self.process.poll() is None:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait()
            self.process = None

        if self._log_file is not None:
            self._log_file.close()
            self._log_file = None
