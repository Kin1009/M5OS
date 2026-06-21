import system

import config_store


_known = []
_open = []

_mode = 'known'
_index = 0

_started = False
_done = False

_timer = 0


# -------------------------
# LOAD SAVED WIFI
# -------------------------


def load_wifi():
    return config_store.load_wifi()


# -------------------------
# START CONNECTION PROCESS
# -------------------------


def start():

    global _known
    global _open
    global _index
    global _mode
    global _started
    global _done
    global _timer

    if _started:
        return

    saved = load_wifi()

    scan = system.wifi_scan()

    if not scan:

        _done = True
        return

    # strongest first
    scan.sort(
        key=lambda ap: ap['rssi'],
        reverse=True
    )

    _known = []
    _open = []

    for ap in scan:

        ssid = ap['ssid']

        # saved network
        if ssid in saved:

            _known.append(
                (
                    ssid,
                    saved[ssid]
                )
            )

        # open network
        elif ap['auth'] == 0:

            _open.append(ssid)

    _started = True
    _done = False

    # start with saved networks
    if _known:

        _mode = 'known'
        _index = 0

        ssid, password = _known[0]

        print(
            "Trying saved:",
            ssid
        )

        system.wifi_connect(
            ssid,
            password
        )

        _timer = 50

    elif _open:

        _mode = 'open'
        _index = 0

        ssid = _open[0]

        print(
            "Trying open:",
            ssid
        )

        system.wifi_connect(
            ssid,
            ''
        )

        _timer = 50

    else:

        _done = True


# -------------------------
# TRY NEXT NETWORK
# -------------------------


def _next_network():

    global _index
    global _mode
    global _timer
    global _done

    if _mode == "known":

        _index += 1

        if _index < len(_known):

            ssid, password = _known[_index]

            print(
                "Trying saved:",
                ssid
            )

            system.wifi_connect(
                ssid,
                password
            )

            _timer = 50
            return

        # switch to open networks

        _mode = 'open'
        _index = 0

        if not _open:

            _done = True
            return

        ssid = _open[0]

        print(
            "Trying open:",
            ssid
        )

        system.wifi_connect(
            ssid,
            ''
        )

        _timer = 50
        return

    # -------------------------
    # OPEN NETWORKS
    # -------------------------

    _index += 1

    if _index >= len(_open):

        _done = True
        return

    ssid = _open[_index]

    print(
        "Trying open:",
        ssid
    )

    system.wifi_connect(
        ssid,
        ''
    )

    _timer = 50


# -------------------------
# UPDATE
# -------------------------


def update():

    global _timer
    global _done

    if not _started:
        return

    if _done:
        return

    state = system.wifi_status()

    if state == "CONNECTED":

        print('Connected')

        _done = True
        return

    if state == "FAIL":

        _next_network()
        return

    _timer -= 1

    if _timer <= 0:

        _next_network()


# -------------------------
# HELPERS
# -------------------------


def connected():
    return system.wifi_status() == 'CONNECTED'



def status():
    return system.wifi_status()



def label():
    return system.wifi_label()



def done():
    return _done
