from pathlib import Path
from datetime import datetime

from core.logger import LogcatLogger


def start_logcat(hu: str, phone: str) -> tuple[LogcatLogger, LogcatLogger]:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = Path("logs") / timestamp
    log_dir.mkdir(parents=True, exist_ok=True)

    hu_logger = LogcatLogger(hu, log_dir / "HU_logcat.txt")
    phone_logger = LogcatLogger(phone, log_dir / "PHONE_logcat.txt")

    print("[INFO] Clearing logcat buffers")
    hu_logger.clear()
    phone_logger.clear()

    print("[INFO] Starting logcat")
    hu_logger.start()
    try:
        phone_logger.start()
    except Exception:
        hu_logger.stop()
        raise

    print(f"[INFO] Logcat files: {log_dir}")
    return hu_logger, phone_logger


def stop_logcat(loggers: tuple[LogcatLogger, LogcatLogger]) -> None:
    for logger in loggers:
        logger.stop()
    print("[INFO] Logcat stopped")
