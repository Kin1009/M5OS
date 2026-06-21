import base64
import json
import os
import requests
import system
import time

import graphics as g

import ui


g.init()

print("\n[BOOT] Firmware updater module loading...")

SETTINGS_PATH = '/flash/config/settings.json'

DEFAULT_SETTINGS = {
    "wifiinput": 0,
    "brightness": 100,
    "autowifi": 1,
    "bootapp": "/flash/apps/startup/startup.py",
    "updaterepo": "Kin1009/M5OS",
    "appstoreip": "0.0.0.0",
    "volume": 75,
    "timezone": "GMT0",
    "forceupdate": 0
}


# =========================
# SETTINGS
# =========================
print("[LOAD] Defining load_settings")


def load_settings():
    print("[CALL] load_settings()")

    try:
        print("[IO] Reading settings file:", SETTINGS_PATH)

        with open(SETTINGS_PATH, 'r') as f:
            cfg = json.load(f)

        print("[OK] Settings loaded from file")

    except Exception as e:
        print("[WARN] Settings load failed, using defaults:", e)
        cfg = {}

    for key, value in DEFAULT_SETTINGS.items():
        if key not in cfg:
            print("[DEFAULT] Missing key:", key, '->', value)
            cfg[key] = value

    print("[DONE] load_settings returning config")
    return cfg


canvas = g.canvas


# =========================
# INPUT WAIT
# =========================
print("[LOAD] Defining wait_any_key")


def wait_any_key():
    print("[CALL] wait_any_key()")

    while True:
        if system.key1_just_pressed():
            print("[INPUT] KEY1 pressed")
            return

        if system.key2_just_pressed():
            print("[INPUT] KEY2 pressed")
            return

        time.sleep_ms(20)


# =========================
# MESSAGE UI
# =========================
print("[LOAD] Defining message()")


def message(lines):
    print("[CALL] message()")

    if isinstance(lines, str):
        lines = [lines]

    print("[UI] message lines count:", len(lines))

    while True:
        canvas.fillScreen(0x000000)
        canvas.setTextColor(0xFFFFFF)

        y = 10

        for i, line in enumerate(lines):
            print("[UI] line", i, ':', line)

            canvas.setCursor(5, y)
            canvas.print(str(line))
            y += 15

        canvas.push(0, 0)

        if system.key1_just_pressed() or system.key2_just_pressed():
            print("[INPUT] exit message()")
            return

        time.sleep_ms(20)


# =========================
# FIRMWARE DECODER
# =========================
print("[LOAD] Defining decode_firmware()")


def decode_firmware(text):
    print("[CALL] decode_firmware()")

    bundle = json.loads(text)
    files = {}
    version = bundle['__numeric_version__']
    open('/flash/config/version', 'w').write(str(version))
    print("[PARSE] keys in bundle:", list(bundle.keys()))

    for path, entry in bundle['files'].items():
        print("[DECODE] file:", path, "| type:", entry['type'])

        if entry['type'] == "text":
            files[path] = entry['data']

        elif entry['type'] == "binary":
            print("[DECODE] base64 decoding:", path)
            files[path] = base64.b64decode(entry['data'])

    print("[DONE] decode_firmware files:", len(files))
    return {
        "version": bundle.get("__version__"),
        "numeric_version": bundle.get("__numeric_version__"),
        "files": files
    }


# =========================
# FILE SYSTEM HELP
# =========================
print("[LOAD] Defining ensure_parent()")


def ensure_parent(path):
    print("[CALL] ensure_parent():", path)

    parts = path.split('/')[:-1]
    current = ''

    for part in parts:
        if not part:
            continue

        current += '/' + part

        try:
            print("[FS] mkdir:", current)
            os.mkdir(current)
        except Exception as e:
            # folder exists usually
            pass


# =========================
# INSTALLER
# =========================
print("[LOAD] Defining install_firmware()")


def install_firmware(fw_path):
    print("\n[CALL] install_firmware() ->", fw_path)

    try:
        print("[IO] Reading firmware bundle")
        with open(fw_path, 'r') as f:
            text = f.read()

        print("[OK] Firmware file read, size:", len(text))

    except Exception as e:
        print("[ERROR] firmware read failed:", e)
        message(["Read failed", str(e)])
        return False

    print("[STEP] decoding firmware")
    bundle = decode_firmware(text)
    files = bundle['files']

    total = len(files)
    current = 0

    print("[STEP] installing files:", total)

    for path, data in files.items():
        current += 1

        print("\n[INSTALL]", current, '/', total)
        print("[PATH]", path)

        if path == "/flash/apps/firmware_updater/core.py":
            print("[SKIP] self updater file")
            continue

        canvas.fillScreen(0x000000)
        canvas.setTextColor(0xFFFFFF)

        canvas.setCursor(5, 5)
        canvas.print("Installing " + str(current) + '/' + str(total))

        canvas.setCursor(5, 25)
        canvas.print(path[-28:])

        canvas.push(0, 0)

        ensure_parent(path)

        try:
            if isinstance(data, str):
                print("[WRITE] text file")
                with open(path, 'w') as f:
                    f.write(data)
            else:
                print("[WRITE] binary file")
                with open(path, 'wb') as f:
                    f.write(data)

            print("[OK] wrote:", path)

        except Exception as e:
            print("[ERROR] write failed:", path, e)
            message(["Install failed", str(e)])
            return False
    
    print("\n[DONE] firmware install complete")
    return True
