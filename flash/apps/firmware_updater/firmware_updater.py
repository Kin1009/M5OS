import ui
import json
import base64
import requests
import graphics as g
import system
import os
import time

UPDATE_URL = (
    "https://raw.githubusercontent.com/"
    "Kin1009/M5OS/main/flash.json"
)

VERSION_FILE = "/flash/config/version"

canvas = g.canvas


def read_version():

    try:

        with open(VERSION_FILE, "r") as f:
            return int(f.read().strip())

    except:

        return 0


def wait_any_key():

    while True:

        if (
            system.key1_just_pressed()
            or
            system.key2_just_pressed()
        ):
            return

        time.sleep_ms(20)


def message(lines):

    if isinstance(lines, str):
        lines = [lines]

    while True:

        canvas.fillScreen(0x000000)

        canvas.setTextColor(0xFFFFFF)

        y = 10

        for line in lines:

            canvas.setCursor(5, y)
            canvas.print(str(line))

            y += 15

        canvas.push(0, 0)

        if (
            system.key1_just_pressed()
            or
            system.key2_just_pressed()
        ):
            return

        time.sleep_ms(20)


def decode_firmware(text):

    bundle = json.loads(text)

    files = {}

    for path, entry in bundle["files"].items():

        if entry["type"] == "text":

            files[path] = entry["data"]

        elif entry["type"] == "binary":

            files[path] = base64.b64decode(
                entry["data"]
            )

    return {
        "version": bundle.get("__version__"),
        "numeric_version":
            bundle.get("__numeric_version__"),
        "files": files
    }


def ensure_parent(path):

    parts = path.split("/")[:-1]

    current = ""

    for part in parts:

        if not part:
            continue

        current += "/" + part

        try:
            os.mkdir(current)
        except:
            pass


def install_firmware(fw):

    files = fw["files"]

    total = len(files)
    current = 0

    for path, data in files.items():

        current += 1

        # updater cannot replace itself
        if (
            path ==
            "/flash/apps/firmware_updater/"
            "firmware_updater.py"
        ):
            continue

        canvas.fillScreen(0x000000)

        canvas.setTextColor(0xFFFFFF)

        canvas.setCursor(5, 5)
        canvas.print(
            "Installing "
            + str(current)
            + "/"
            + str(total)
        )

        canvas.setCursor(5, 25)
        canvas.print(path[-28:])

        canvas.push(0, 0)

        ensure_parent(path)

        try:

            if isinstance(data, str):

                with open(path, "w") as f:
                    f.write(data)

            else:

                with open(path, "wb") as f:
                    f.write(data)

        except Exception as e:

            message([
                "Install failed",
                str(e)
            ])

            return False

    with open(VERSION_FILE, "w") as f:
        f.write(
            str(fw["numeric_version"])
        )

    return True


def check_for_updates():

    try:

        canvas.fillScreen(0x000000)

        canvas.setCursor(5, 5)
        canvas.print(
            "Downloading..."
        )

        canvas.push(0, 0)

        r = requests.get(
            UPDATE_URL
        )

        if r.status_code != 200:

            message([
                "Download failed",
                str(r.status_code)
            ])

            return

        fw = decode_firmware(
            r.text
        )

        local_ver = read_version()

        remote_ver = (
            fw["numeric_version"]
        )

        if remote_ver <= local_ver:

            message([
                "Up to date!",
                "",
                "K1/K2 return"
            ])

            return

        choice = ui.chooser(
            [
                "New version: "
                + str(remote_ver),
                "Install",
                "Cancel"
            ],
            label="Update"
        )

        if choice != 1:
            return

        ok = install_firmware(
            fw
        )

        if ok:

            message([
                "Update complete",
                "Version "
                + str(remote_ver),
                "",
                "Restart device"
            ])

    except Exception as e:

        message([
            "Update failed",
            str(e)
        ])


def firmware_updater():

    while True:

        version = read_version()

        choice = ui.chooser(
            [
                "Version: "
                + str(version),
                "Check for updates",
                "Exit"
            ],
            label="Firmware Updater"
        )

        if choice == 0:
            continue

        elif choice == 1:
            check_for_updates()

        elif choice == 2:
            return


firmware_updater()
