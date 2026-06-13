import os
import json

import graphics as g
import system
from M5 import Widgets
import time
BTN_W = 108
BTN_H = 39

APPS_PER_PAGE = 6

POSITIONS = [
    (0, 0),
    (120, 0),
    (0, 47),
    (120, 47),
    (0,   94),
    (120, 94),
]


class AppButton(g.UIObject):

    def __init__(self, name, x, y, selected=False):
        self.name = name
        self.x = x
        self.y = y
        self.selected = selected

    def draw(self, c):

        # shadow border
        c.drawRect(
            self.x + 2,
            self.y + 2,
            BTN_W,
            BTN_H,
            0x0B1A0F if not self.selected else 0x4bab65
        )
        g.Rectangle(
            0x000000,
            self.x,
            self.y,
            BTN_W - 1,
            BTN_H - 1
        ).draw(c)
        # main border
        c.drawRect(
            self.x,
            self.y,
            BTN_W,
            BTN_H,
            0x0B1A0F if not self.selected else 0x4bab65
        )

        # selected fill
        if self.selected:
            c.fillRect(
                self.x + 1,
                self.y + 1,
                BTN_W - 2,
                BTN_H - 2,
                0x4bab65
            )

        # text
        c.setFont(Widgets.FONTS.Montserrat12)

        text = self.name

        try:
            text_w = c.textWidth(text)
        except:
            # fallback approximation if API missing
            text_w = len(text) * 6

        text_h = 12  # Montserrat12 approx height

        tx = self.x + (BTN_W - text_w) // 2
        ty = self.y + (BTN_H + text_h) // 2 - 12
        c.setTextColor(0xFFFFFF, (0x000000 if not self.selected else 0x4bab65))
        c.setCursor(tx, ty)
        c.print(text)
class PageIndicator(g.UIObject):

    def __init__(self, page, total):
        self.page = page
        self.total = total

    def draw(self, c):

        txt = "%d/%d" % (self.page + 1, self.total)

        c.setTextColor(0xFFFFFF)

        text_w = len(txt) * 8

        c.setCursor(
            (240 - text_w) // 2,
            1
        )

        c.print(txt)


def discover_apps():

    apps = []

    try:
        folders = os.listdir("/flash/apps")
    except:
        return [{
            "name": "Return",
            "path": None
        }]

    for folder in folders:

        if folder in ("startup", "apps", "return"):
            continue

        try:

            with open("/flash/apps/%s/config.json" % folder) as f:
                cfg = json.load(f)

            apps.append({
                "name": cfg.get("name", folder),
                "path": cfg.get("path", "")
            })

        except:
            pass

    apps.append({
        "name": "Return",
        "path": None
    })

    return apps


def chooser():
    global exit_chooser
    apps = discover_apps()

    if not apps:
        return None

    index = 0

    total_pages = (
        len(apps) + APPS_PER_PAGE - 1
    ) // APPS_PER_PAGE

    while True:
        if check_exit():
            exit_chooser = 1
            break
        if system.key2_just_pressed():

            index += 1

            if index >= len(apps):
                index = 0

        if system.key1_just_pressed():

            return apps[index]

        page = index // APPS_PER_PAGE

        start = page * APPS_PER_PAGE
        end = min(
            start + APPS_PER_PAGE,
            len(apps)
        )

        page_apps = apps[start:end]

        selected_on_page = index % APPS_PER_PAGE

        scene = []

        for i, app in enumerate(page_apps):

            x, y = POSITIONS[i]

            scene.append(
                AppButton(
                    app["name"],
                    x,
                    y,
                    selected=(i == selected_on_page)
                )
            )

        scene.append(
            PageIndicator(
                page,
                total_pages
            )
        )

        g.update(scene)
        g.render()
exit_hold_start = None
exit_chooser = 0
def check_exit():
    global exit_hold_start

    if system.key1_pressed() and system.key2_pressed():

        if exit_hold_start is None:
            exit_hold_start = time.ticks_ms()

        elif time.ticks_diff(time.ticks_ms(), exit_hold_start) > 2000:
            return True

    else:
        exit_hold_start = None

    return False

while True:
    app = chooser()
    if exit_chooser:
        break
    time.sleep(0.05)
    if (app and app.get("path")) and (not system.key2_pressed()):
        system.safe_run_app(app["path"])
    else:
        break

print("done")