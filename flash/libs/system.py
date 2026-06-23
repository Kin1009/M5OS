import gc
import sys
import time
import io
import network
import ntptime

import M5
from M5 import *

from audio import Player
from machine import Pin

import config_store
import graphics as g
from hardware import IR
import ui


print("[debug] system boot start")

_last_ntp_sync = 0


def ntp_sync():
    #print("[debug] ntp_sync")

    global _last_ntp_sync

    if _wifi_state != "CONNECTED":
        #print("[debug] ntp_sync skipped (wifi not connected)")
        return False

    try:
        ntptime.host = "time.google.com"
        #print("[debug] ntp host =", ntptime.host)

        ntptime.settime()

        _last_ntp_sync = time.time()

        #print("[debug] ntp sync success")
        return True

    except Exception as e:
        print("[debug] ntp sync failed:", e)
        return False


print("[debug] M5.begin()")
M5.begin()

print("[debug] WLAN init")
_wlan = network.WLAN(network.STA_IF)

_wifi_state = "OFF"
_wifi_ssid = None
_wifi_start_time = 0

print("[debug] loading settings")
cfg = config_store.load_settings()

_volume = cfg.get("volume", 75)

print("[debug] volume =", _volume)

print("[debug] audio init")
player = Player(None)

Mic.end()
Speaker.end()
Speaker.setPA(True)

print("[debug] audio ready")


def exception_to_string(exc):
    print("[debug] exception_to_string")

    try:
        s = io.StringIO()
        sys.print_exception(exc, s)
        return s.getvalue()
    except Exception:
        return str(exc)


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

K1 = Pin(11, Pin.IN, Pin.PULL_UP)
K2 = Pin(12, Pin.IN, Pin.PULL_UP)


def key1_pressed():
    return K1.value() == 0


def key2_pressed():
    return K2.value() == 0


def key1_just_pressed():
    global _k1_prev, player

    current = K1.value()

    pressed = (_k1_prev == 1 and current == 0)

    _k1_prev = current

    if pressed:
        player.play_tone(
            2000,
            0.1,
            volume=_volume,
            sync=False
        )

    return pressed


def key2_just_pressed():
    global _k2_prev, player

    current = K2.value()

    pressed = (_k2_prev == 1 and current == 0)

    if pressed:
        player.play_tone(
            1500,
            0.1,
            volume=_volume,
            sync=False
        )

    _k2_prev = current

    return pressed


def safe_run_app(path):
    print("[debug] safe_run_app")
    print("[debug] path =", repr(path))

    try:
        gc.collect()

        print("[debug] reading app")

        with open(path, "r") as f:
            code = f.read()

        print("[debug] app size =", len(code))

        app_globals = {
            "__name__": "__main__",
            "__file__": path,
        }

        print("[debug] executing app")

        exec(code, app_globals, app_globals)

        print("[debug] app exited")

    except Exception as e:
        err = exception_to_string(e)

        print(err)

        ui.chooser(
            err.split("\n"),
            label="Exception"
        )

    finally:
        gc.collect()
        print("[debug] gc collected")


def wifi_scan():
    print("[debug] wifi_scan")

    try:
        _wlan.active(True)

        aps = []
        seen = set()

        for ap in _wlan.scan():

            try:
                ssid = ap[0].decode()

            except:
                ssid = str(ap[0])

            if ssid in seen:
                continue

            seen.add(ssid)

            aps.append({
                "ssid": ssid,
                "rssi": ap[3],
                "auth": ap[4]
            })

        print("[debug] wifi_scan found", len(aps), "aps")

        return aps

    except Exception as e:
        print("[debug] wifi_scan failed:", e)
        return []


def wifi_connect(ssid, password):
    global _wifi_state
    global _wifi_ssid
    global _wifi_start_time
    global _wlan

    print("[debug] wifi_connect")
    print("[debug] ssid =", repr(ssid))

    _wifi_ssid = ssid
    _wifi_state = "CONNECTING"

    try:
        _wlan.disconnect()
        time.sleep_ms(100)

    except Exception as e:
        print("[debug] disconnect:", e)

    try:
        _wlan.active(False)
        time.sleep_ms(100)

    except Exception as e:
        print("[debug] disable wlan:", e)

    try:
        _wlan.active(True)
        time.sleep_ms(200)

    except Exception as e:
        print("[debug] enable wlan:", e)

    try:
        _wlan.connect(ssid, password)

    except OSError as e:
        _wifi_state = "FAIL"
        print("[debug] wifi connect failed:", e)
        return

    _wifi_start_time = time.ticks_ms()

    print("[debug] wifi connection started")


def wifi_update():
    global _wifi_state

    if _wifi_state != "CONNECTING":
        return

    if _wlan.isconnected():
        _wifi_state = "CONNECTED"

        try:
            print(
                "[debug] wifi connected ip =",
                _wlan.ifconfig()[0]
            )
        except:
            print("[debug] wifi connected")

        return

    if time.ticks_diff(
        time.ticks_ms(),
        _wifi_start_time
    ) > 10000:

        _wifi_state = "FAIL"

        print("[debug] wifi timeout")


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
    #print("[debug] get_timezone_offset")

    try:
        cfg = config_store.load_settings()

        tz = cfg.get(
            "timezone",
            "GMT0"
        )

        #print("[debug] timezone =", tz)

    except Exception as e:
        print("[debug] timezone read failed:", e)
        return 0

    if tz == "GMT0":
        return 0

    try:
        return int(tz[3:])

    except Exception as e:
        print("[debug] invalid timezone:", e)
        return 0


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

    except Exception as e:
        print("[debug] time_label failed:", e)
        return "--:--"

def wifi_ssid():
    return _wifi_ssid
print("[debug] system boot complete")