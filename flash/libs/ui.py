from graphics import *
import graphics as g
from system import *
import time
import system
import os
# -------------------------
# UI THEME (GLOBAL)
# -------------------------
WIDTH = 240
HEIGHT = 135
THEME = {
    "bg": 0x444444,
    "fg": 0xFFFFFF,
    "accent": 0x4bab65,   # selected highlight
    "muted": 0x666666,
    "border": 0xFFFFFF,
    "input_bg": 0x333333,
    "button_bg": 0x000000,
    "button_sel": 0x4bab65,
}
class Chooser(UIObject):
    def __init__(self, items, x, y, fg=0xFFFFFF, bg=None):
        self.items = items
        self.index = 0
        self.x = x
        self.y = y
        self.fg = fg
        self.bg = bg

    def next(self):
        self.index += 1

        if self.index >= len(self.items):
            self.index = 0

    def prev(self):
        self.index -= 1

        if self.index < 0:
            self.index = len(self.items) - 1

    def get(self):
        return self.index

    def draw(self, c):

        visible_items = 10

        start = max(0, self.index - 5)
        end = min(start + visible_items, len(self.items))

        if end - start < visible_items:
            start = max(0, end - visible_items)

        for screen_row, item_index in enumerate(range(start, end)):

            item = self.items[item_index]
            item_y = self.y + (screen_row * 13)

            if item_index == self.index:

                if self.bg is not None:
                    c.setTextColor(self.fg, self.bg)
                else:
                    c.setTextColor(self.fg)

                c.setCursor(self.x, item_y)
                c.print("> " + str(item))

            else:

                c.setTextColor(self.fg)
                c.setCursor(self.x, item_y)
                c.print("  " + str(item))
def wrap_text(text, width):
    lines = []

    text = str(text)

    while len(text) > width:
        lines.append(text[:width])
        text = text[width:]

    lines.append(text)

    return lines
def index_to_y(index, length):

    if length <= 1:
        return 67

    return 1 + (index * 132) // (length - 1)
def chooser(
    items,
    label=None,
    scroll_after=7,
    wrap_after=22,
    x=0,
    y=0,
    fg=0xFFFFFF,
    bg=0x4bab65,
    index=0
):

    LINE_H = 15

    while True:

        # -------------------------
        # INPUT
        # -------------------------
        if system.key2_just_pressed():
            index = (index + 1) % len(items)

        if system.key1_just_pressed():
            return index

        canvas = g.canvas
        canvas.fillScreen(THEME["bg"])

        # -------------------------
        # HEADER
        # -------------------------
        list_y = y

        if label is not None:
            canvas.setTextColor(THEME["fg"], THEME["bg"])
            canvas.setCursor(x, y)
            canvas.print(str(label))
            list_y += 16

        # -------------------------
        # PRE-COMPUTE ITEM BLOCK HEIGHTS
        # -------------------------
        wrapped_items = []
        item_heights = []

        for item in items:
            lines = wrap_text(str(item), wrap_after)
            wrapped_items.append(lines)
            item_heights.append(len(lines))

        # -------------------------
        # SCROLL POSITION (PIXEL-BASED)
        # -------------------------
        max_visible_lines = scroll_after

        # compute pixel Y for selected item
        selected_pixel_y = 0
        for i in range(index):
            selected_pixel_y += item_heights[i] * LINE_H

        start_pixel = max(0, selected_pixel_y - (max_visible_lines // 2) * LINE_H)

        # -------------------------
        # RENDER LIST
        # -------------------------
        y_cursor = list_y
        pixel_cursor = 0

        for item_i, lines in enumerate(wrapped_items):

            item_block_height = len(lines) * LINE_H

            # skip above viewport
            if pixel_cursor + item_block_height < start_pixel:
                pixel_cursor += item_block_height
                continue

            # stop if below viewport
            if y_cursor > HEIGHT - 10:
                break

            for line_i, line in enumerate(lines):

                if pixel_cursor < start_pixel:
                    pixel_cursor += LINE_H
                    continue

                item_y = y_cursor

                is_selected = (item_i == index and line_i == 0)

                if is_selected:
                    canvas.setTextColor(THEME["fg"], THEME["accent"])
                    canvas.setCursor(x, item_y)
                    canvas.print("> " + line)
                else:
                    canvas.setTextColor(THEME["fg"], THEME["bg"])
                    canvas.setCursor(x, item_y)
                    canvas.print("  " + line)

                y_cursor += LINE_H
                pixel_cursor += LINE_H

        # -------------------------
        # SCROLLBAR
        # -------------------------
        for i in range(135):
            if i % 2 == 0:
                canvas.fillRect(230, i, 1, 1, fg)

        if len(items) <= 1:
            bar_y = 0
        else:
            bar_y = int((index * (135 - 10)) / (len(items) - 1))

        canvas.fillRect(229, bar_y, 3, 10, THEME["fg"])
        # -------------------------
        # FRACTION LABEL
        # -------------------------
        frac = f"{index + 1}/{len(items)}"
        text_w = canvas.textWidth(frac)

        fx = 240 - text_w - 18
        fy = max(bar_y - 4, 0)

        canvas.setTextColor(THEME["fg"], THEME["bg"])
        canvas.setCursor(fx, fy)
        canvas.print(frac)

        canvas.push(0, 0)
def draw_button(canvas, label, x, y, selected=False):
    color = 0xFFFFFF
    bg = THEME["button_bg"]

    if selected:
        bg = THEME["button_sel"]

    # border
    canvas.fillRect(x, y, BTN_W, BTN_H, bg)
    canvas.drawRect(x, y, BTN_W, BTN_H, color)

    # text (center-ish)
    canvas.setFont(Widgets.FONTS.ASCII7)
    canvas.setTextColor(color, bg)
    canvas.setCursor(x + 10, y + 12)
    canvas.print(label)
    canvas.setFont(Widgets.FONTS.Montserrat12)
def keypad(prompt="Enter number"):
    input_str = ""
    index = 0

    while True:
        # -------------------------
        # INPUT
        # -------------------------
        if system.key2_just_pressed():  # switch
            index += 1
            if index >= len(KEYS):
                index = 0

        if system.key1_just_pressed():  # OK/select
            key = KEYS[index]

            if key == "OK":
                return input_str

            elif key == "Del":
                input_str = input_str[:-1]

            else:
                input_str += key

        # -------------------------
        # RENDER
        # -------------------------
        canvas = g.canvas
        canvas.fillScreen(0x000000)

        # display box
        canvas.fillRect(5, 22, 230, 20, THEME["input_bg"])
        canvas.drawRect(5, 22, 230, 20, THEME["border"])
        canvas.setCursor(5, 2)
        canvas.print(prompt)
        canvas.setTextColor(0xFFFFFF)
        canvas.setCursor(10, 30)
        canvas.print(input_str)

        # draw buttons (3x4 grid)
        for i in range(12):
            row = i // 6
            col = i % 6

            x = START_X + col * BTN_W
            y = START_Y + row * BTN_H

            draw_button(canvas, KEYS[i], x, y, selected=(i == index))

        canvas.push(0, 0)
KEYS = [
    "1","2","3",
    "4","5","6",
    "7","8","9",
    "0", "Del","OK"
]
BTN_W = 39
BTN_H = 39

START_X = 5
START_Y = 50
INPUT_BTN_W = 45
INPUT_BTN_H = 25

INPUT_KEYS = [
    "ABCDEF",
    "GHIJKL",
    "MNOPQR",
    "STUVWX",
    "YZ",

    "01234",
    "56789",

    "+-*/^",
    "()[];",
    "{}.,/",
    "!@#$%",
    "&_=:\\",

    "Shift",
    "Del",
    "OK"
]

def button_label(key):

    if key in ("Shift", "Del", "OK"):
        return key

    if len(key) > 1:
        return key[0] + "-" + key[-1]

    return key
def draw_input_button(canvas, label, x, y, selected=False):

    color = 0xFFFFFF
    bg = THEME["button_bg"]

    if selected:
        bg = THEME["button_sel"]

    canvas.fillRect(
        x,
        y,
        INPUT_BTN_W,
        INPUT_BTN_H,
        bg
    )

    canvas.drawRect(
        x,
        y,
        INPUT_BTN_W,
        INPUT_BTN_H,
        color
    )

    canvas.unloadFont()

    canvas.setTextColor(color, bg)

    text_w = len(label) * 8

    canvas.setCursor(
        x + (INPUT_BTN_W - text_w) // 2,
        y + 9
    )

    canvas.print(label)

    canvas.setFont(
        Widgets.FONTS.Montserrat12
    )
import json
import network
import socket
import time
import graphics as g


HTML = """\
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{
    background:#111;
    color:#fff;
    font-family:sans-serif;
    margin:20px;
}
h2{
    margin-bottom:10px;
}
input{
    width:100%;
    padding:12px;
    font-size:18px;
    box-sizing:border-box;
}
button{
    width:100%;
    padding:12px;
    margin-top:10px;
    font-size:18px;
}
</style>
</head>
<body>

<h2>%PROMPT%</h2>

<form method="POST">
<input
    name="text"
    autocomplete="off"
    autofocus
>
<button type="submit">
Submit
</button>
</form>

</body>
</html>
"""


def wifi_input(prompt="Enter text:"):

    canvas = g.canvas

    ap = network.WLAN(network.AP_IF)
    ap.active(True)

    ap.config(
        essid="StickS3",
        authmode=network.AUTH_OPEN
    )

    ip = ap.ifconfig()[0]

    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    server = socket.socket()

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    server.listen(1)

    result = None

    try:

        while result is None:

            # -------------------------
            # CANCEL INPUT
            # -------------------------
            if system.key1_just_pressed() or system.key2_just_pressed():
                result = ""
                break

            # -------------------------
            # SCREEN
            # -------------------------
            canvas.fillScreen(0x000000)
            canvas.setTextColor(0xFFFFFF)

            canvas.setCursor(5, 10)
            canvas.print("WiFi Hotspot Input")

            canvas.setCursor(5, 30)
            canvas.print("SSID: StickS3")

            canvas.setCursor(5, 50)
            canvas.print("Open in browser:")

            canvas.setCursor(5, 70)
            canvas.print("http://" + ip)

            canvas.setCursor(5, 95)
            canvas.print(prompt)

            canvas.push(0, 0)

            # -------------------------
            # SOCKET
            # -------------------------
            server.settimeout(0.1)

            try:
                client, addr = server.accept()
            except:
                continue

            try:
                request = client.recv(2048).decode()

                if request.startswith("POST"):

                    body = request.split("\r\n\r\n", 1)[1]

                    if "text=" in body:

                        text = body.split("text=", 1)[1]
                        text = text.split("&", 1)[0]
                        text = url_decode(text)

                        result = text

                        client.send(
                            "HTTP/1.1 200 OK\r\n"
                            "Content-Type: text/html\r\n\r\n"
                            "<h2>Saved. You can close this page.</h2>"
                        )

                    else:
                        client.send("HTTP/1.1 400 OK\r\n\r\n")

                else:

                    page = HTML.replace("%PROMPT%", prompt)

                    client.send(
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html\r\n\r\n"
                    )
                    client.send(page)

            except:
                pass

            try:
                client.close()
            except:
                pass

    finally:

        try:
            server.close()
        except:
            pass

        try:
            ap.active(False)
        except:
            pass

    return result
def url_decode(s):

    s = s.replace("+", " ")

    out = ""
    i = 0

    while i < len(s):

        if s[i] == "%" and i + 2 < len(s):

            try:
                out += chr(
                    int(
                        s[i + 1:i + 3],
                        16
                    )
                )

                i += 3
                continue

            except:
                pass

        out += s[i]
        i += 1

    return out
def input(prompt="Enter text:"):

    try:

        with open(
            "/flash/config/settings.json",
            "r"
        ) as f:

            settings = json.load(f)

        wifiinput = settings.get(
            "wifiinput",
            0
        )

    except:

        wifiinput = 0

    if wifiinput:

        return wifi_input(prompt)

    return local_input(prompt)
def local_input(prompt="Enter text:"):
    text = ""

    group_index = 0
    char_index = 0

    shift = True

    last_hold = time.ticks_ms()
    subtracted = 0

    k1_down_time = None
    space_inserted = False

    while True:

        # -------------------------
        # K2 short press
        # -------------------------

        if system.key2_just_pressed():

            group_index += 1

            if group_index >= len(INPUT_KEYS):
                group_index = 0

            char_index = 0

        # -------------------------
        # K2 hold = cycle character
        # -------------------------

        now = time.ticks_ms()

        if system.key2_pressed():

            if time.ticks_diff(now, last_hold) > 150:

                if not subtracted:

                    group_index -= 1

                    if group_index < 0:
                        group_index = len(INPUT_KEYS) - 1

                    subtracted = 1

                key = INPUT_KEYS[group_index]

                if key not in (
                    "Shift",
                    "Del",
                    "OK"
                ):

                    char_index += 1

                    if char_index >= len(key):
                        char_index = 0

                last_hold = now

        else:

            last_hold = now
            subtracted = 0

        # -------------------------
        # K1 hold = space
        # -------------------------

        if system.key1_pressed():

            if k1_down_time is None:
                k1_down_time = now

            elif (
                not space_inserted and
                time.ticks_diff(
                    now,
                    k1_down_time
                ) > 500
            ):

                text += " "
                space_inserted = True

        else:

            k1_down_time = None
            space_inserted = False

        # -------------------------
        # K1 press
        # -------------------------

        if system.key1_just_pressed():

            key = INPUT_KEYS[group_index]

            if key == "OK":

                return text

            elif key == "Del":

                text = text[:-1]

            elif key == "Shift":

                shift = not shift

            else:

                char = key[char_index]

                if shift:
                    char = char.upper()
                else:
                    char = char.lower()

                text += char

        # -------------------------
        # Render
        # -------------------------

        canvas = g.canvas

        canvas.fillScreen(0x000000)

        canvas.setTextColor(0xFFFFFF)

        canvas.setCursor(5, 2)
        canvas.print(prompt)

        # input box

        canvas.fillRect(
            5,
            22,
            230,
            20,
            0x000000
        )

        canvas.drawRect(
            5,
            22,
            230,
            20,
            0xFFFFFF
        )

        canvas.setCursor(10, 25)
        canvas.print(text)

        # preview

        preview = INPUT_KEYS[group_index]

        if preview not in (
            "Shift",
            "Del",
            "OK"
        ):

            preview = preview[char_index]

            if not preview.isdigit():

                if shift:
                    preview = preview.upper()
                else:
                    preview = preview.lower()

        canvas.setCursor(180, 2)
        canvas.print("[" + preview + "]")

        # shift indicator

        canvas.setCursor(150, 2)

        if shift:
            canvas.print("ABC")
        else:
            canvas.print("abc")

        # buttons

        for i in range(len(INPUT_KEYS)):

            row = i // 5
            col = i % 5

            x = 5 + col * INPUT_BTN_W
            y = 50 + row * INPUT_BTN_H

            label = INPUT_KEYS[i]

            if label == "Shift":

                if shift:
                    label = "ABC"
                else:
                    label = "abc"

            else:

                label = button_label(label)
            draw_input_button(
                canvas,
                label,
                x,
                y,
                selected=(i == group_index)
            )

        canvas.push(0, 0)
def _is_dir(path):

    try:
        os.listdir(path)
        return True

    except:
        return False


def _parent_dir(path):

    if path == "/":
        return "/"

    parts = path.rstrip("/").split("/")

    if len(parts) <= 1:
        return "/"

    return "/".join(parts[:-1]) or "/"


def dirchooser(start="/flash"):

    cwd = start

    while True:

        entries = []

        entries.append("[Select This Folder]")

        if cwd == "/flash":
            entries.append("Exit")

        elif cwd != "/":
            entries.append("..")

        try:

            names = sorted(
                os.listdir(cwd)
            )

        except:

            names = []

        for name in names:

            full = cwd + "/" + name

            if _is_dir(full):

                entries.append(
                    "[D] " + name
                )

        choice = chooser(
            entries,
            label=cwd
        )

        selected = entries[choice]

        if selected == "[Select This Folder]":
            return cwd

        if selected == "Exit":
            return None

        if selected == "..":

            cwd = _parent_dir(cwd)
            continue

        if selected.startswith("[D] "):

            dirname = selected[4:]

            cwd = cwd + "/" + dirname
def _parent(path):

    if path in ("/", "/flash"):
        return path

    parts = path.rstrip("/").split("/")
    if len(parts) <= 1:
        return "/"

    return "/".join(parts[:-1]) or "/"


def getfile(start="/flash"):

    cwd = start

    while True:

        entries = []

        if cwd != "/flash":
            entries.append("..")
        entries.append("[New file]")
        try:
            names = sorted(os.listdir(cwd))
        except:
            names = []

        for n in names:

            full = cwd + "/" + n

            if _is_dir(full):
                entries.append("[D] " + n)
            else:
                entries.append(n)

        entries.append("[Cancel]")

        choice = chooser(
            entries,
            label="Pick file: " + cwd
        )

        selected = entries[choice]
        # -------------------------
        # New file
        # -------------------------
        if selected == "[New file]":

            name = input("File name")

            if not name:
                continue

            path = cwd + "/" + name

            # create empty file
            try:
                with open(path, "w") as f:
                    f.write("")
            except:
                pass

            return path
        # -------------------------
        # Cancel
        # -------------------------

        if selected == "[Cancel]":
            return None

        # -------------------------
        # Parent dir
        # -------------------------

        if selected == "..":
            cwd = _parent(cwd)
            continue

        # -------------------------
        # Directory enter
        # -------------------------

        if selected.startswith("[D] "):
            cwd = cwd + "/" + selected[4:]
            continue

        # -------------------------
        # File selected
        # -------------------------

        return cwd + "/" + selected