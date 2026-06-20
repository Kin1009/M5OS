import ui
import system
import config_store
from M5 import *


# -------------------------
# SETTINGS LOAD / SAVE
# -------------------------

DEFAULT_SETTINGS = config_store.DEFAULT_SETTINGS


def load_settings():
    return config_store.load_settings()


def save_settings(cfg):

    try:
        config_store.save_settings(cfg)

    except Exception as e:

        print(system.exception_to_string(e))

        ui.chooser(
            system.exception_to_string(e).split("\n"),
            label="Exception"
            )


# -------------------------
# WIFI LOAD / SAVE
# -------------------------

def load_wifi():
    return config_store.load_wifi()


def save_wifi(cfg):

    try:
        config_store.save_wifi(cfg)

    except:
        pass


# -------------------------
# WIFI MENU
# -------------------------

def wifi_menu():

    while True:

        cfg = load_wifi()

        ssids = list(cfg.keys())

        menu = ssids + ["[Add]", "[Exit]"]

        choice = ui.chooser(
            menu,
            label="WiFi"
        )

        selected = menu[choice]

        if selected == "[Exit]":
            return

        if selected == "[Add]":

            ssid = ui.input("SSID")

            if not ssid:
                continue

            password = ui.input("Password")

            if password is None:
                continue

            cfg[ssid] = password

            save_wifi(cfg)

            continue

        action = ui.chooser(
            ["Connect", "Modify", "Delete", "Back"],
            label=selected
        )

        if action == 3:
            continue

        elif action == 0:

            system.wifi_connect(
                selected,
                cfg[selected]
            )

        elif action == 1:

            password = ui.input(
                "Password"
            )

            if password is not None:

                cfg[selected] = password

                save_wifi(cfg)

        elif action == 2:

            try:

                del cfg[selected]

                save_wifi(cfg)

            except:
                pass


# -------------------------
# ABOUT
# -------------------------
import time
import network
import system
import graphics as g
import gc
from M5 import Power


def safe(fn, default="N/A"):
    try:
        return fn()
    except:
        return default

def read_version():

    try:

        with open(
            "/flash/config/version",
            "r"
        ) as f:

            return int(
                f.read().strip()
            )

    except:

        return 0
def about_menu():

    canvas = g.canvas

    wlan_sta = network.WLAN(network.STA_IF)
    wlan_ap = network.WLAN(network.AP_IF)

    last_update = 0
    scroll = 0

    LINE_H = 12
    VISIBLE_LINES = 10

    info = []

    while True:

        now = time.ticks_ms()

        # -------------------------
        # INPUT
        # -------------------------

        if system.key1_just_pressed():
            scroll = max(0, scroll - 1)

        if system.key2_just_pressed():
            scroll += 1

        # hold both keys to exit
        if system.key1_pressed() and system.key2_pressed():
            return


        # -------------------------
        # UPDATE EVERY 500MS
        # -------------------------

        if time.ticks_diff(now, last_update) > 500:

            info = [

                "=== STICKS3 INFO ===",

                "",
                "STA IP : %s" % safe(lambda: wlan_sta.ifconfig()[0]),
                "AP IP  : %s" % safe(lambda: wlan_ap.ifconfig()[0]),

                "",
                "=== POWER ===",

                "Battery   : %d%%" % Power.getBatteryLevel(),
                "Voltage   : %.2fV" % Power.getBatteryVoltage(),
                "Charging  : %s" % ("Yes" if Power.isCharging() else "No"),

                "",
                "VBUS      : %.2fV" % Power.getVBUSVoltage(),
                "Ext OUT   : %s" % Power.getExtOutput(),
                "Ext USB V : %.2fV" % Power.getExtVoltage(Power.PORT.USB),
                "Ext A V   : %.2fV" % Power.getExtVoltage(Power.PORT.A),

                "",
                "=== WIFI ===",

                "WiFi State : %s" % system.wifi_label(),

                "",
                "=== MEMORY ===",

                "Free GC   : %s" % format_bytes(gc.mem_free()),
                "Alloc GC  : %s" % format_bytes(gc.mem_alloc()),

                "",
                "=== FIRMWARE ===",

                "Version   : %d" % read_version(),

                "",
                "=== SYSTEM ===",

                "Uptime ms : %d" % time.ticks_ms(),
                "",
                "Hold K1+K2 to exit"
            ]
            last_update = now


        # -------------------------
        # SCROLL LIMIT
        # -------------------------

        max_scroll = max(0, len(info) - VISIBLE_LINES)
        if scroll > max_scroll:
            scroll = max_scroll


        # -------------------------
        # RENDER
        # -------------------------

        canvas.fillScreen(0x000000)
        canvas.setTextColor(0xFFFFFF)

        y = 5

        for i in range(scroll, len(info)):

            canvas.setCursor(5, y)
            canvas.print(info[i])

            y += LINE_H

            if y > 135:
                break


        # scroll indicator
        canvas.setCursor(200, 5)
        canvas.print("%d/%d" % (scroll + 1, max_scroll + 1 if max_scroll >= 0 else 1))

        canvas.push(0, 0)

        time.sleep_ms(50)
def format_bytes(val):

    units = ["B", "KB", "MB"]
    idx = 0

    value = float(val)

    while value >= 1024 and idx < len(units) - 1:
        value /= 1024
        idx += 1

    return "{:.3f} {}".format(value, units[idx])
# -------------------------
# SETTINGS MENU
# -------------------------

def settings_app():
    choice = 0
    while True:

        cfg = load_settings()

        menu = [

            "WiFi",

            "WiFi Input: " +
            ("On" if cfg["wifiinput"] else "Off"),

            "Brightness: %d%%" % cfg["brightness"],

            "Volume: %d%%" % cfg["volume"],

            "Timezone: " + cfg["timezone"],

            "Auto WiFi: " +
            ("On" if cfg["autowifi"] else "Off"),

            "Boot App",
            "Update Repo",
            "Force Update: " + ("On" if cfg["forceupdate"] else "Off"),
            "App Store IP",
            "About",
            "Exit"
        ]

        choice = ui.chooser(
            menu,
            label="Settings",
            index=choice
        )

        # WiFi

        if choice == 0:
            wifi_menu()

        # WiFi Input

        elif choice == 1:

            cfg["wifiinput"] = (
                1 - cfg["wifiinput"]
            )

            save_settings(cfg)

        # Brightness

        elif choice == 2:

            cfg["brightness"] += 5

            if cfg["brightness"] > 100:
                cfg["brightness"] = 5
            Widgets.setBrightness(int(255 * cfg["brightness"] / 100))
            save_settings(cfg)
        # Volume
        elif choice == 3:

            cfg["volume"] += 5

            if cfg["volume"] > 100:
                cfg["volume"] = 0

            save_settings(cfg)
            system._volume = cfg["volume"]
        # Timezone
        elif choice == 4:

            tz = cfg["timezone"]

            if tz == "GMT0":
                offset = 0
            else:
                offset = int(tz[3:])

            offset += 1

            if offset > 12:
                offset = -12

            if offset == 0:
                cfg["timezone"] = "GMT0"
            elif offset > 0:
                cfg["timezone"] = "GMT+" + str(offset)
            else:
                cfg["timezone"] = "GMT" + str(offset)
            time.timezone(cfg["timezone"])
            save_settings(cfg)
        # Auto WiFi

        elif choice == 5:

            cfg["autowifi"] = (
                1 - cfg["autowifi"]
            )

            save_settings(cfg)

        # Boot App

        elif choice == 6:

            value = ui.input(
                "Boot App"
            )

            if value is not None:

                cfg["bootapp"] = value

                save_settings(cfg)

        # Update Repo

        elif choice == 7:

            value = ui.input(
                "Update Repo"
            )

            if value is not None:

                cfg["updaterepo"] = value

                save_settings(cfg)
        # Force Update
        elif choice == 8:

            cfg["forceupdate"] = (
                1 - cfg["forceupdate"]
            )

            save_settings(cfg)
        # App Store IP

        elif choice == 9:

            value = ui.input(
                "App Store IP"
            )

            if value is not None:

                cfg["appstoreip"] = value

                save_settings(cfg)

        # About

        elif choice == 10:

            about_menu()

        # Exit

        elif choice == 11:

            return


settings_app()
