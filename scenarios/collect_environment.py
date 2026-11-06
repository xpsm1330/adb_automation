# scenarios/collect_environment.py

from pathlib import Path

def adb_query():
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    hu_commands = [
            "getprop ro.build.id",
            "getprop ro.build.display.id",
            "getprop ro.build.version.incremental",
            "getprop ro.build.fingerprint"
        ]
    
    hu_file = out / "hu_configuration.txt"

    with open(hu_file, "w", encoding="utf-8") as f:
        f.write("=== HU CONFIGURATION ===\n\n")

        for cmd in hu_commands:
            f.write(f"$ {cmd}\n")
            f.write(adb.shell(hu_serial, cmd))
            f.write("\n\n")

    print(f"[INFO] {hu_file.name}")


def collect_environment(adb, hu_serial, phone_serial, output_dir="evidence"):
    """
    Collects:
    - HU configuration
    - Phone configuration
    - User/profile information
    - DCSM status
    - Test start timestamp
    """

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    print("[INFO] Collecting environment information...")

    # ============================================================
    # HU CONFIGURATION
    # ============================================================

    hu_commands = [
        "getprop ro.build.id",
        "getprop ro.build.display.id",
        "getprop ro.build.version.incremental",
        "getprop ro.build.fingerprint"
    ]

    hu_file = out / "hu_configuration.txt"

    with open(hu_file, "w", encoding="utf-8") as f:
        f.write("=== HU CONFIGURATION ===\n\n")

        for cmd in hu_commands:
            f.write(f"$ {cmd}\n")
            f.write(adb.shell(hu_serial, cmd))
            f.write("\n\n")

    print(f"[INFO] {hu_file.name}")

    # ============================================================
    # PHONE CONFIGURATION
    # ============================================================

    phone_commands = [
        "getprop ro.product.manufacturer",
        "getprop ro.product.model",
        "getprop ro.build.version.release",
        "getprop ro.build.version.sdk",
        "getprop ro.build.fingerprint"
    ]

    phone_file = out / "phone_configuration.txt"

    with open(phone_file, "w", encoding="utf-8") as f:
        f.write("=== PHONE CONFIGURATION ===\n\n")

        for cmd in phone_commands:
            f.write(f"$ {cmd}\n")
            f.write(adb.shell(phone_serial, cmd))
            f.write("\n\n")

    print(f"[INFO] {phone_file.name}")

    # ============================================================
    # ACTIVE USER
    # ============================================================

    current_user_file = out / "current_user.txt"

    with open(current_user_file, "w", encoding="utf-8") as f:
        f.write(adb.shell(hu_serial, "am get-current-user"))

    print(f"[INFO] {current_user_file.name}")

    # ============================================================
    # USER LIST
    # ============================================================

    users_file = out / "users.txt"

    with open(users_file, "w", encoding="utf-8") as f:
        f.write(adb.shell(hu_serial, "pm list users"))

    print(f"[INFO] {users_file.name}")

    # ============================================================
    # DUMPSYS USER
    # ============================================================

    dumpsys_users_file = out / "dumpsys_user.txt"

    with open(dumpsys_users_file, "w", encoding="utf-8") as f:
        f.write(adb.shell(hu_serial, "dumpsys user"))

    print(f"[INFO] {dumpsys_users_file.name}")

    # ============================================================
    # DCSM
    # ============================================================

    dcsm_file = out / "dcsm.txt"

    with open(dcsm_file, "w", encoding="utf-8") as f:
        f.write(
            adb.shell(
                hu_serial,
                "dumpsys activity services com.harman.DCSM"
            )
        )

    print(f"[INFO] {dcsm_file.name}")

    # ============================================================
    # TIMESTAMP
    # ============================================================

    timestamp_file = out / "test_start_time.txt"

    with open(timestamp_file, "w", encoding="utf-8") as f:

        f.write("=== HU DATE ===\n")
        f.write(adb.shell(hu_serial, "date"))

        f.write("\n\n=== HU EPOCH ===\n")
        f.write(adb.shell(hu_serial, "date +%s"))

    print(f"[INFO] {timestamp_file.name}")

    print("[INFO] Environment collection completed.")