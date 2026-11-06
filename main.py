from core.adb import AdbDevice
from core.utils import create_evidence_dir
evidence_dir = create_evidence_dir("before")
from scenarios.collect_users import collect_users
from scenarios.collect_connection_scope import collect_connection_scope
from scenarios.collect_environment import collect_environment
from core.utils import AdbHelper, load_devices
from scenarios.start_logcat import start_logcat
adb = AdbHelper()
devices = load_devices()
HU = devices["hu"]["serial"]
PHONE = devices["phone"]["serial"]

AdbDevice.verify_device(HU)
device = AdbDevice("HU")

print(f"HU={HU}")
print(f"PHONE={PHONE}")

result = adb.shell(HU, "getprop ro.build.id")
print(f"Build ID: {result}")

start_logcat(HU,PHONE)

collect_environment(
    adb=adb,
    hu_serial=HU,
    phone_serial=PHONE,
    output_dir=(f'{evidence_dir}/env_setup')
)

collect_users(
    device=device,
    output_dir=evidence_dir / "users"
)

collect_connection_scope(
    device=device,
    output_dir=evidence_dir / "connection_scope",
    phase="before"
)