import json
import time
import system
import graphics as g
import ui

PATH = "/flash/apps/calendar/data.json"

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

FONT_PATH = "/system/common/font/Montserrat-Medium-10.vlw"

SCREEN_H = 135


# -------------------------
# STORAGE
# -------------------------

def load():
    try:
        with open(PATH, "r") as f:
            return json.load(f)
    except:
        return {"groups": [], "events": []}


def save(data):
    try:
        with open(PATH, "w") as f:
            json.dump(data, f)
    except:
        pass


# -------------------------
# COLORS
# -------------------------

def parse_color(c):
    if isinstance(c, int):
        return c
    if isinstance(c, str):
        if c.startswith("#"):
            return int(c[1:], 16)
        if c.startswith("0x"):
            return int(c[2:], 16)
        return int(c)
    return 0xFFFFFF


def group_map(data):
    m = {}
    for g in data["groups"]:
        m[g["id"]] = parse_color(g.get("color", "#FFFFFF"))
    return m


# -------------------------
# TIME HELPERS
# -------------------------

def time_key(t):
    try:
        h, m = t.split(":")
        return int(h) * 60 + int(m)
    except:
        return 0


def day_events(data, day):
    ev = []
    for e in data["events"]:
        if day in e.get("days", []):
            ev.append(e)

    ev.sort(key=lambda x: time_key(x.get("start", "00:00")))
    return ev


def get_today_index():
    try:
        return time.localtime()[6] % 7
    except:
        return 0


# -------------------------
# HEIGHT ESTIMATION (for scroll start)
# -------------------------

def estimate_height(data):
    h = 0

    for i in range(7):
        h += 16

        ev = 0
        for e in data["events"]:
            if i in e.get("days", []):
                ev += 1

        if ev == 0:
            h += 14
        else:
            h += ev * 10

        h += 6

    return h


# -------------------------
# DRAW WEEK UI
# -------------------------

def draw_week(data, scroll):
    c = g.canvas
    c.fillScreen(0x050505)

    c.loadFont(FONT_PATH)

    colors = group_map(data)
    today = get_today_index()

    y = 5 - scroll

    for i, day in enumerate(DAYS):

        # -------------------------
        # DAY CARD BACKGROUND
        # -------------------------
        card_h = 14

        bg = 0x111111
        if i == today:
            bg = 0x222244

        #c.fillRect(0, y - 2, 240, card_h, bg)

        # -------------------------
        # DAY TITLE
        # -------------------------
        c.setTextColor(0xFFFFFF, 0x050505)
        c.setCursor(4, y)
        c.print("[" + day + "]")

        y += 14

        events = day_events(data, i)

        if not events:

            c.setTextColor(0x555555, 0x050505)
            c.setCursor(10, y)
            c.print("No events")

            y += 12

        else:

            for e in events:

                col = colors.get(e.get("group", ""), 0xFFFFFF)

                # event background bar
                c.fillRect(6, y + 1, 228, 10, 0x101010)

                c.setTextColor(col, 0x101010)
                c.setCursor(10, y)

                text = e.get("start", "--:--") + " " + e.get("title", "")
                c.print(text)

                y += 12

        y += 6

    c.push(0, 0)
    c.unloadFont()


# -------------------------
# ADD EVENT
# -------------------------

def add_event(data):

    title = ui.input("Event name")
    if not title:
        return

    group = ui.input("Group id")
    if not group:
        group = "default"

    days_raw = ui.input("Days (0-6 comma)")
    start = ui.input("Start HH:MM")
    end = ui.input("End HH:MM")

    days = []
    try:
        for d in days_raw.split(","):
            d = d.strip()
            if d:
                days.append(int(d))
    except:
        pass

    data["events"].append({
        "id": title.lower().replace(" ", "_"),
        "title": title,
        "group": group,
        "days": days,
        "start": start or "00:00",
        "end": end or "00:00",
        "repeat": True
    })


# -------------------------
# MENU
# -------------------------

def menu():
    return ui.chooser(
        ["Week View", "Add Event", "Exit"],
        label="Calendar"
    )


# -------------------------
# MAIN APP
# -------------------------

def calendar_app():

    data = load()

    while True:

        choice = menu()

        # -------------------------
        # WEEK VIEW
        # -------------------------
        if choice == 0:

            scroll = get_today_index() * 40

            max_scroll = max(0, estimate_height(data) - SCREEN_H)

            while True:

                draw_week(data, scroll)

                time.sleep(0.05)

                # EXIT (K1)
                if system.key1_just_pressed():
                    break

                # SCROLL (K2)
                if system.key2_just_pressed():
                    scroll += 12

                    if scroll > max_scroll:
                        scroll = 0

        # -------------------------
        # ADD EVENT
        # -------------------------
        elif choice == 1:
            add_event(data)
            save(data)

        # -------------------------
        # EXIT APP
        # -------------------------
        else:
            return


# -------------------------
# RUN
# -------------------------

calendar_app()