from pathlib import Path
from datetime import datetime
from core.logger import LogcatLogger


def start_logcat(hu, phone):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    log_dir = Path("logs") / timestamp
    log_dir.mkdir(parents=True, exist_ok=True)

    hu_log = log_dir / "HU_logcat.txt"
    phone_log = log_dir / "PHONE_logcat.txt"

    hu_logger = LogcatLogger(
        hu,
        hu_log
    )

    phone_logger = LogcatLogger(
        phone,
        phone_log
    )

    print("[INFO] Clearing logcat buffers")

    hu_logger.clear()
    phone_logger.clear()

    print("[INFO] Starting logcat")

    hu_logger.start()
    phone_logger.start()

    try:

        print()
        print("===================================")
        print("Logging started")
        print("Press CTRL+C to stop")
        print("===================================")

        while True:
            pass

    except KeyboardInterrupt:

        print()
        print("[INFO] Stopping loggers")

        hu_logger.stop()
        phone_logger.stop()

        print(f"[INFO] Logs saved to {log_dir}")