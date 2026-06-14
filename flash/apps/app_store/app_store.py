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
def install_repo_name(repo):

    try:

        repo_name = repo.split("/")[-1]

        app_name = repo_name

        if app_name.startswith("m5os_"):
            app_name = app_name[5:]

        url = (
            "https://raw.githubusercontent.com/"
            + repo
            + "/main/"
            + app_name
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
            label=app_name + " v" + version
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

            if isinstance(data, bytes):

                with open(dest, "wb") as f:
                    f.write(data)

            else:

                with open(dest, "w") as f:
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
def install_repo():

    repo = ui.input(
        "Repo (user/repo)"
    )

    if not repo:
        return

    install_repo_name(repo)
def install_from_list():

    try:

        with open(
            "/flash/apps/app_store/applist",
            "r"
        ) as f:

            repos = []

            for line in f:

                line = line.strip()

                if line:
                    repos.append(line)

    except Exception as e:

        ui.chooser(
            ["OK"],
            label=str(e)
        )

        return

    if not repos:

        ui.chooser(
            ["OK"],
            label="No apps"
        )

        return

    labels = []

    for repo in repos:

        name = repo.split("/")[-1]

        if name.startswith("m5os_"):
            name = name[5:]

        labels.append(name)

    labels.append("Cancel")

    choice = ui.chooser(
        labels,
        label="Apps"
    )

    if choice >= len(repos):
        return

    install_repo_name(
        repos[choice]
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
                "Install from list",
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

        elif choice == 2:

            install_from_list()

        else:

            return


app_store()