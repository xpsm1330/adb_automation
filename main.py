from core.adb import AdbDevice
from core.utils import AdbHelper, create_evidence_dir, load_devices
from scenarios.collect_build_info import collect_build_info
from scenarios.collect_connection_scope import collect_connection_scope
from scenarios.collect_environment import collect_environment
from scenarios.collect_users import collect_users
from scenarios.start_logcat import start_logcat, stop_logcat


def main():
    evidence_dir = create_evidence_dir("before")
    devices = load_devices()
    hu_serial = devices["hu"]["serial"]
    phone_serial = devices["phone"]["serial"]

    AdbDevice.verify_device(hu_serial)
    AdbDevice.verify_device(phone_serial)

    hu_device = AdbDevice(hu_serial)
    adb = AdbHelper()
    print(f"HU={hu_serial}")
    print(f"PHONE={phone_serial}")

    loggers = start_logcat(hu_serial, phone_serial)
    try:
        collect_build_info(hu_device, evidence_dir / "build_info")
        collect_environment(
            adb=adb,
            hu_serial=hu_serial,
            phone_serial=phone_serial,
            output_dir=evidence_dir / "env_setup",
        )
        collect_users(hu_device, evidence_dir / "users")
        collect_connection_scope(
            device=hu_device,
            output_dir=evidence_dir / "connection_scope",
            phase="before",
        )

        input("Collection complete. Press Enter or Ctrl+C to stop logcat... ")
    except KeyboardInterrupt:
        print("\n[INFO] Stop requested")
    finally:
        stop_logcat(loggers)
        print(f"[INFO] Evidence saved to {evidence_dir}")


if __name__ == "__main__":
    main()
