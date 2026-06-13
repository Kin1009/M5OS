import requests
import json
import base64
import os
import ui
import graphics as g

g.init()

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def mkdir_p(path):

    parts = path.split("/")

    current = ""

    for part in parts:

        if not part:
            continue

        current += "/" + part

        try:
            os.mkdir(current)
        except:
            pass


def parent(path):

    parts = path.split("/")

    return "/".join(parts[:-1])


def show_log(text):

    c = g.canvas

    c.fillScreen(0x000000)

    c.setTextColor(0xFFFFFF)

    c.setCursor(5, 5)
    c.print("Installing...")

    lines = []

    while len(text) > 28:
        lines.append(text[:28])
        text = text[28:]

    lines.append(text)

    y = 25

    for line in lines:

        c.setCursor(5, y)
        c.print(line)

        y += 15

    c.push(0, 0)

    print("[APPSTORE]", text)


# --------------------------------------------------
# FIRMWARE DECODER
# --------------------------------------------------

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
        "numeric_version": bundle.get(
            "__numeric_version__"
        ),
        "files": files
    }


# --------------------------------------------------
# INSTALL APP
# --------------------------------------------------

def install_repo():

    repo = ui.input(
        "Repo (user/repo)"
    )

    if not repo:
        return

    try:

        repo_name = repo.split("/")[-1]

        url = (
            "https://raw.githubusercontent.com/"
            + repo
            + "/main/"
            + repo_name
            + ".json"
        )

        print("[APPSTORE] Repo:", repo)
        print("[APPSTORE] URL :", url)

        show_log("Downloading...")

        r = requests.get(url)

        print("[APPSTORE] Status:", r.status_code)

        if r.status_code != 200:

            ui.chooser(
                ["OK"],
                label="Repo not found"
            )

            return

        bundle = decode_firmware(r.text)

        version = str(
            bundle.get(
                "numeric_version",
                "?"
            )
        )

        choice = ui.chooser(
            [
                "Install",
                "Cancel"
            ],
            label=repo_name + " v" + version
        )

        if choice == 1:
            return

        files = bundle["files"]

        count = 0

        for path, data in files.items():

            dest = "/flash/apps" + path

            show_log(dest)

            print(
                "[APPSTORE] INSTALL",
                dest
            )

            mkdir_p(
                parent(dest)
            )

            if isinstance(
                data,
                bytes
            ):

                with open(
                    dest,
                    "wb"
                ) as f:

                    f.write(data)

            else:

                with open(
                    dest,
                    "w"
                ) as f:

                    f.write(data)

            count += 1

        print(
            "[APPSTORE] Installed",
            count,
            "files"
        )

        ui.chooser(
            ["OK"],
            label="Installed!"
        )

    except Exception as e:

        print(
            "[APPSTORE] ERROR",
            repr(e)
        )

        ui.chooser(
            ["OK"],
            label=str(e)
        )


# --------------------------------------------------
# MAIN MENU
# --------------------------------------------------

def app_store():

    while True:

        choice = ui.chooser(
            [
                "Browse apps",
                "Install from repo",
                "Exit"
            ],
            label="App Store"
        )

        if choice == 0:

            ui.chooser(
                ["OK"],
                label="Not implemented"
            )

        elif choice == 1:

            install_repo()

        else:

            return


app_store()