from pathlib import Path


def collect_environment(adb, hu_serial, phone_serial, output_dir="evidence"):
    """Collect basic HU, phone, user, DCSM, and timestamp evidence."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    print("[INFO] Collecting environment information...")

    sections = {
        "hu_configuration.txt": (
            "=== HU CONFIGURATION ===",
            hu_serial,
            [
                "getprop ro.build.id",
                "getprop ro.build.display.id",
                "getprop ro.build.version.incremental",
                "getprop ro.build.fingerprint",
            ],
        ),
        "phone_configuration.txt": (
            "=== PHONE CONFIGURATION ===",
            phone_serial,
            [
                "getprop ro.product.manufacturer",
                "getprop ro.product.model",
                "getprop ro.build.version.release",
                "getprop ro.build.version.sdk",
                "getprop ro.build.fingerprint",
            ],
        ),
    }

    for filename, (title, serial, commands) in sections.items():
        with (out / filename).open("w", encoding="utf-8") as file:
            file.write(f"{title}\n\n")
            for command in commands:
                file.write(f"$ {command}\n")
                file.write(adb.shell(serial, command))
                file.write("\n\n")
        print(f"[INFO] {filename}")

    hu_files = {
        "current_user.txt": "am get-current-user",
        "users.txt": "pm list users",
        "dumpsys_user.txt": "dumpsys user",
        "dcsm.txt": "dumpsys activity services com.harman.DCSM",
    }
    for filename, command in hu_files.items():
        (out / filename).write_text(
            adb.shell(hu_serial, command), encoding="utf-8"
        )
        print(f"[INFO] {filename}")

    with (out / "test_start_time.txt").open("w", encoding="utf-8") as file:
        file.write("=== HU DATE ===\n")
        file.write(adb.shell(hu_serial, "date"))
        file.write("\n\n=== HU EPOCH ===\n")
        file.write(adb.shell(hu_serial, "date +%s"))

    print("[INFO] test_start_time.txt")
    print("[INFO] Environment collection completed.")
