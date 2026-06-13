import json
import system

_networks = []
_index = 0
_started = False
_done = False
_timer = 0


def load_wifi():

    try:
        with open("/flash/config/wifi.json", "r") as f:
            cfg = json.load(f)

        if not isinstance(cfg, dict):
            return []

        return list(cfg.items())

    except:
        return []


def start():

    global _networks, _index, _started, _done, _timer

    if _started:
        return

    _networks = load_wifi()

    if not _networks:
        _done = True
        return

    _index = 0
    _started = True
    _done = False
    _timer = 120

    ssid, password = _networks[0]

    system.wifi_connect(ssid, password)


def update():

    global _index, _timer, _done

    if not _started or _done:
        return

    state = system.wifi_status()

    if state == "CONNECTED":
        _done = True
        return

    if state == "FAIL":
        _timer = 0

    _timer -= 1

    if _timer > 0:
        return

    _index += 1

    if _index >= len(_networks):
        _done = True
        return

    ssid, password = _networks[_index]

    system.wifi_connect(ssid, password)

    _timer = 120


def connected():
    return system.wifi_status() == "CONNECTED"


def status():
    return system.wifi_status()


def label():
    return system.wifi_label()


def done():
    return _done