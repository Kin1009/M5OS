import json
import time
import system
import graphics as g
import ui
from hardware import IR

PATH = "/flash/apps/ir/remotes.json"

# -------------------------
# GLOBAL IR INSTANCE
# -------------------------

ir = None
last_rx = None


def init_ir():
    global ir
    if ir is None:
        ir = IR()
        ir.rx_cb(ir_rx_event)
        ir.tx(0, 0)

 
# -------------------------
# IR CALLBACK
# -------------------------

def ir_rx_event(data, addr, ctrl):
    global last_rx
    last_rx = (data, addr)


# -------------------------
# STORAGE
# -------------------------

def load_data():
    try:
        with open(PATH, "r") as f:
            return json.load(f)
    except:
        return {"items": []}


def save_data(data):
    try:
        with open(PATH, "w") as f:
            json.dump(data, f)
    except:
        pass


# -------------------------
# SIMPLE SCREEN LOG
# -------------------------

def log(msg):
    c = g.canvas
    c.fillScreen(0)
    c.setTextColor(0xFFFFFF)
    c.setCursor(5, 5)
    c.print(str(msg))
    c.push(0, 0)


# -------------------------
# WAIT FOR IR SIGNAL
# -------------------------

def wait_ir():
    global last_rx
    last_rx = None

    init_ir()

    log("Point remote at StickS3")
    time.sleep(1)

    timeout = 200  # ~10s

    while timeout > 0:

        if system.key1_pressed() or system.key2_pressed():
            return None

        if last_rx is not None:
            return last_rx

        time.sleep_ms(50)
        timeout -= 1

    return None


# -------------------------
# RECEIVE MODE
# -------------------------

def receive_mode():

    data = load_data()

    result = wait_ir()

    if not result:
        log("No signal")
        time.sleep_ms(800)
        return

    ir_data, ir_addr = result

    name = ui.input("Name IR signal")

    if not name:
        return

    data["items"].append({
        "name": name,
        "address": ir_addr,
        "command": ir_data
    })

    save_data(data)

    log("Saved: " + name)
    time.sleep_ms(800)


# -------------------------
# TRANSMIT MODE
# -------------------------

def transmit_mode():

    data = load_data()
    items = data.get("items", [])

    if not items:
        ui.chooser(["No signals"], label="IR TX")
        return

    names = [i["name"] for i in items]

    choice = ui.chooser(names + ["Back"], label="Transmit")

    if choice == len(names):
        return

    item = items[choice]

    init_ir()

    try:
        ir.tx(item["address"], item["command"])
        log("Sent: " + item["name"])
        time.sleep_ms(500)
    except Exception as e:
        log("TX FAIL: " + str(e))
        time.sleep_ms(800)


# -------------------------
# MAIN MENU
# -------------------------

def main_menu():
    return ui.chooser(
        ["Transmit", "Receive", "Exit"],
        label="IR Remote"
    )


# -------------------------
# APP LOOP
# -------------------------

def ir_app():

    init_ir()

    while True:

        choice = main_menu()

        if choice == 0:
            transmit_mode()

        elif choice == 1:
            receive_mode()

        else:
            return


ir_app()