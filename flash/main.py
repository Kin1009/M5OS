import time
import json
import os
import ui
import graphics as g
import system
from graphics import *
from M5 import *
import sys

Power.setBatteryCharge(True)

print(os.getcwd())
print(os.listdir("/"))

g.init()

canvas = g.canvas

BOOT_APP = None
BRIGHTNESS = 100


# -------------------------
# LOAD SETTINGS
# -------------------------
try:
    with open("/flash/config/settings.json", "r") as f:
        cfg = json.load(f)

    BOOT_APP = cfg.get("bootapp", "")
    BRIGHTNESS = cfg.get("brightness", 100)

except:
    cfg = {}


# -------------------------
# APPLY BRIGHTNESS
# -------------------------
try:
    b = max(0, min(100, int(BRIGHTNESS)))
    Widgets.setBrightness(b * 255 // 100)
except:
    pass
exit_repl = 0

# -------------------------
# REPL ESCAPE SCREEN
# -------------------------
canvas.fillScreen(0x000000)
canvas.setTextColor(0xFFFFFF)
canvas.setCursor(10, 60)
canvas.print("Press K1 or K2 to exit to REPL.")

canvas.push(0, 0)

start = time.ticks_ms()

while time.ticks_diff(time.ticks_ms(), start) < 2500:

    if system.key1_pressed() or system.key2_pressed():
        exit_repl = 1
        g.init()
        break

if not exit_repl:
# -------------------------
    # STARTUP ROUTING
    # -------------------------
    DEFAULT_STARTUP = "/flash/apps/startup/startup.py"
    target = BOOT_APP if BOOT_APP else DEFAULT_STARTUP


    def launch(app_path):
        try:
            system.safe_run_app(app_path)
        finally:
            import sys
            sys.exit()


    launch(target)
