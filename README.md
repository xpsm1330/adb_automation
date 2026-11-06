# adb_automation

ADB-based tool for collecting Android device logs and diagnostic evidence.

## Requirements

- Python 3.10 or newer
- Android Platform Tools (`adb`) installed and available on `PATH`
- USB debugging enabled and both configured devices authorized

Install Python dependencies with `python -m pip install -r requirements.txt`.

## Configure devices

Edit `config/devices.yaml` and set the ADB serials for `hu` and `phone`.
Do not commit real device identifiers if they are sensitive; use a local-only
configuration or environment-specific setup where appropriate.

## Run

From the repository root, run:

```bash
python main.py
```

The script starts logcat for both devices, collects build/environment/user and
connection-scope evidence, then waits for Enter or Ctrl+C to stop logging.
Files are written below `logs/`.
