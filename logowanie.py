from core.utils import AdbHelper, load_devices
from scenarios.start_logcat import start_logcat
adb = AdbHelper()

devices = load_devices()
HU = devices["hu"]["serial"]
PHONE = devices["phone"]["serial"]

start_logcat(HU,PHONE)
