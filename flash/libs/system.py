import M5
from M5 import *
from machine import Pin
import time
import graphics as g
import sys
import gc
import io
import ui
import network
from hardware import IR
from audio import Player
import ntptime
import config_store

_last_ntp_sync = 0

def ntp_sync():

    global _last_ntp_sync

    if _wifi_state != "CONNECTED":
        return False

    try:

        ntptime.host = "time.google.com"
        ntptime.settime()

        _last_ntp_sync = time.time()

        return True

    except Exception as e:

        print("NTP:", e)

        return False
M5.begin()
_wlan = network.WLAN(network.STA_IF)

_wifi_state = "OFF"   # OFF, CONNECTING, CONNECTED, FAIL
_wifi_ssid = None
_wifi_start_time = 0
_volume = 0
cfg = config_store.load_settings()
_volume = cfg.get("volume", 75)
player = Player(None)
Mic.end()
Speaker.end()
Speaker.setPA(True)
def exception_to_string(exc):

    s = io.StringIO()

    sys.print_exception(exc, s)

    return s.getvalue()
_k1_prev = 1
_k2_prev = 1
def battery_level():
    try:
        if hasattr(Power, "getBatteryLevel"):
            return Power.getBatteryLevel()
        elif hasattr(Power, "getBatteryPercent"):
            return Power.getBatteryPercent()
        else:
            return -1
    except:
        return -1

# -------------------------
# GPIO mapping
# -------------------------
K1 = Pin(11, Pin.IN, Pin.PULL_UP)  # G11
K2 = Pin(12, Pin.IN, Pin.PULL_UP)  # G12
def key1_pressed():
    # active-low button assumption
    return K1.value() == 0
def key2_pressed():
    # active-low button assumption
    return K2.value() == 0
def key1_just_pressed():
    global _k1_prev, player

    current = K1.value()

    pressed = (_k1_prev == 1 and current == 0)
    _k1_prev = current
    if pressed:
        #Speaker.setVolume(-1)
        #Speaker.playWav("/system/common/wav/click.wav")
        #player.play("/system/common/wav/click.wav", pos=0, volume=_volume, sync=True)
        player.play_tone(2000, 0.1, volume=_volume, sync=False)
    return pressed
def key2_just_pressed():
    global _k2_prev, player

    current = K2.value()

    pressed = (_k2_prev == 1 and current == 0)
    if pressed:
        #Speaker.setVolume(_volume)
        #player.play("/system/common/wav/click.wav", pos=0, volume=_volume, sync=True)
        player.play_tone(1500, 0.1, volume=_volume, sync=False)
    _k2_prev = current
    return pressed
def safe_run_app(path):

    print("path =", repr(path))

    try:

        gc.collect()

        with open(path, "r") as f:
            code = f.read()

        app_globals = {
            "__name__": "__main__",
            "__file__": path,
        }

        exec(code, app_globals, app_globals)

    except Exception as e:

        print(exception_to_string(e))

        ui.chooser(
            exception_to_string(e).split("\n"),
            label="Exception"
        )
def wifi_scan():

    try:

        _wlan.active(True)

        aps = []

        for ap in _wlan.scan():

            try:
                ssid = ap[0].decode()
            except:
                ssid = str(ap[0])

            aps.append({
                "ssid": ssid,
                "rssi": ap[3],
                "auth": ap[4]
            })

        return aps

    except Exception as e:

        print("WiFi scan failed:", e)

        return []
def wifi_connect(ssid, password):
    global _wifi_state, _wifi_ssid, _wifi_start_time, _wlan

    _wifi_ssid = ssid
    _wifi_state = "CONNECTING"

    try:
        _wlan.disconnect()
        time.sleep_ms(100)
    except:
        pass

    try:
        _wlan.active(False)
        time.sleep_ms(100)
    except:
        pass

    try:
        _wlan.active(True)
        time.sleep_ms(200)
    except:
        pass

    try:
        _wlan.connect(ssid, password)

    except OSError as e:
        _wifi_state = "ERROR"
        print("WiFi connect failed:", e)
        return

    _wifi_start_time = time.ticks_ms()

    _wifi_start_time = time.ticks_ms()
def wifi_update():
    global _wifi_state

    if _wifi_state != "CONNECTING":
        return

    if _wlan.isconnected():
        _wifi_state = "CONNECTED"
        return

    if time.ticks_diff(
        time.ticks_ms(),
        _wifi_start_time
    ) > 10000:
        _wifi_state = "FAIL"
def wifi_status():
    return _wifi_state


def wifi_label():
    if _wifi_state == "CONNECTED":
        return "C"
    elif _wifi_state == "CONNECTING":
        return "..."
    else:
        return "NC"
def get_timezone_offset():

    try:
        cfg = config_store.load_settings()

        tz = cfg.get("timezone", "GMT0")

    except:

        return 0

    if tz == "GMT0":
        return 0

    return int(tz[3:])
def time_label():
    try:

        t = time.localtime()

        h = t[3] + get_timezone_offset()
        m = t[4]

        if h < 0:
            h += 24

        if h >= 24:
            h -= 24

        return "%02d:%02d" % (h, m)

    except:

        return "--:--"
