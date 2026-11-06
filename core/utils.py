from pathlib import Path
from datetime import datetime
import yaml, subprocess


def timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def create_evidence_dir(phase: str) -> Path:
    """
    Tworzy katalog:
    logs/<phase>_<timestamp>
    """

    folder = Path("logs") / f"{phase}_{timestamp()}"
    folder.mkdir(parents=True, exist_ok=True)

    return folder


def write_file(output_dir, filename, content):
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path

def load_devices():
    with open("config/devices.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["devices"]

class AdbHelper:
    def shell(self, serial, command):
        result = subprocess.run(
            ["adb", "-s", serial, "shell", command],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"ADB command failed:\n{result.stderr}"
            )

        return result.stdout