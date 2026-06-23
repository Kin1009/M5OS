import base64
import json
import os
import requests
import system
import time

import graphics as g

import ui

def get_remote_numeric_version():
    try:
        repo = load_settings().get(
            "updaterepo",
            "Kin1009/M5OS"
        )

        url = (
            "https://raw.githubusercontent.com/"
            + repo
            + "/main/NUMERIC_VERSION"
        )

        r = requests.get(url)

        if r.status_code != 200:
            return None

        return int(r.text.strip())

    except:
        return None
    
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


def load_settings():

    try:

        with open(
            SETTINGS_PATH,
            'r'
        ) as f:

            cfg = json.load(f)

    except:

        cfg = {}

    for key, value in DEFAULT_SETTINGS.items():

        if key not in cfg:

            cfg[key] = value

    return cfg

def get_update_url():

    try:

        with open(
            '/flash/config/settings.json',
            'r'
        ) as f:

            settings = json.load(f)

        repo = settings.get(
            'updaterepo',
            'Kin1009/M5OS'
        )

    except:

        repo = 'Kin1009/M5OS'

    return (
        'https://raw.githubusercontent.com/'
        + repo +
        '/main/flash.json'
    )

VERSION_FILE = '/flash/config/version'

canvas = g.canvas

def get_numeric_version_url():

    try:

        with open(
            SETTINGS_PATH,
            "r"
        ) as f:

            settings = json.load(f)

        repo = settings.get(
            "updaterepo",
            "Kin1009/M5OS"
        )

    except:

        repo = "Kin1009/M5OS"

    return (
        "https://raw.githubusercontent.com/"
        + repo +
        "/main/NUMERIC_VERSION"
    )

def read_version():

    try:

        with open(VERSION_FILE, 'r') as f:
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
def download_with_progress(url, title):
    r = requests.get(url, stream=True)

    try:

        if r.status_code != 200:
            raise Exception(
                "HTTP " +
                str(r.status_code)
            )

        total = int(
            r.headers.get(
                "Content-Length",
                "0"
            )
        )

        received = 0
        chunks = []

        while True:

            if system.key1_just_pressed():

                try:
                    r.close()
                except:
                    pass

                message([
                    "Download",
                    "cancelled"
                ])

                return None

            chunk = r.raw.read(1024)

            if not chunk:
                break

            chunks.append(chunk)

            received += len(chunk)

            percent = 0

            if total:
                percent = (
                    received * 100
                ) // total

            canvas.fillScreen(
                0x000000
            )

            canvas.setTextColor(
                0xFFFFFF
            )

            canvas.setCursor(5, 5)
            canvas.print(title)

            canvas.setCursor(5, 25)
            canvas.print(
                str(percent)
                + "%"
            )

            canvas.setCursor(5, 45)
            canvas.print("WiFi:")

            canvas.setCursor(5, 60)
            canvas.print(
                str(
                    system.wifi_ssid()
                )
            )

            canvas.setCursor(5, 90)
            canvas.print(
                "K1 Cancel"
            )

            canvas.push(0, 0)

        return b"".join(chunks)

    finally:

        try:
            r.close()
        except:
            pass


def decode_firmware(text):

    bundle = json.loads(text)

    files = {}

    for path, entry in bundle['files'].items():

        if entry['type'] == "text":

            files[path] = entry['data']

        elif entry['type'] == "binary":

            files[path] = base64.b64decode(
                entry['data']
            )

    return {
        "version": bundle.get("__version__"),
        "numeric_version":
            bundle.get('__numeric_version__'),
        "files": files
    }



def ensure_parent(path):

    parts = path.split('/')[:-1]

    current = ''

    for part in parts:

        if not part:
            continue

        current += '/' + part

        try:
            os.mkdir(current)
        except:
            pass



def install_firmware(fw):

    files = fw['files']

    total = len(files)
    current = 0

    for path, data in files.items():

        current += 1

        # updater cannot replace itself
        if (
            path ==
            '/flash/apps/firmware_updater/'
            'firmware_updater.py'
        ):
            continue

        canvas.fillScreen(0x000000)

        canvas.setTextColor(0xFFFFFF)

        canvas.setCursor(5, 5)
        canvas.print(
            "Installing "
            + str(current)
            + '/'
            + str(total)
        )

        canvas.setCursor(5, 25)
        canvas.print(path[-28:])

        canvas.push(0, 0)

        ensure_parent(path)

        try:

            if isinstance(data, str):

                with open(path, 'w') as f:
                    f.write(data)

            else:

                with open(path, 'wb') as f:
                    f.write(data)

        except Exception as e:

            message([
                "Install failed",
                str(e)
            ])

            return False

    with open(VERSION_FILE, 'w') as f:
        f.write(
            str(fw['numeric_version'])
        )

    return True


def check_for_updates():

    try:

        local_ver = read_version()

        version_data = (
            download_with_progress(
                get_numeric_version_url(),
                "Checking Version"
            )
        )

        if version_data is None:
            return

        remote_ver = int(
            version_data.decode().strip()
        )

        settings = load_settings()

        force_update = settings.get(
            "forceupdate",
            0
        )

        if (
            remote_ver <= local_ver
            and
            not force_update
        ):

            message([
                "Up to date!",
                "",
                "Current: "
                + str(local_ver)
            ])

            return

        choice = ui.chooser(
            [
                "Current: "
                + str(local_ver),

                "Remote: "
                + str(remote_ver),

                "Install",

                "Cancel"
            ],
            label="Update"
        )

        if choice != 2:
            return

        fw_data = (
            download_with_progress(
                get_update_url(),
                "Downloading FW"
            )
        )

        if fw_data is None:
            return

        fw = decode_firmware(
            fw_data.decode()
        )

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
                'Exit'
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

