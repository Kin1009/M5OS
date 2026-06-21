import json


SETTINGS_PATH = '/flash/config/settings.json'
WIFI_PATH = '/flash/config/wifi.json'

DEFAULT_SETTINGS = {
    "wifiinput": 0,
    "brightness": 100,
    "autowifi": 1,
    "bootapp": "/flash/apps/startup/startup.py",
    "updaterepo": "Kin1009/M5OS",
    "forceupdate": 0,
    "appstoreip": "0.0.0.0",
    "volume": 75,
    "timezone": "GMT+7"
}



def load_json(path, default=None):
    if default is None:
        default = {}

    try:
        with open(path, 'r') as f:
            data = json.load(f)

        return data

    except:
        return default



def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)



def load_settings():
    cfg = load_json(SETTINGS_PATH, {})

    if not isinstance(cfg, dict):
        cfg = {}

    for key in DEFAULT_SETTINGS:
        if key not in cfg:
            cfg[key] = DEFAULT_SETTINGS[key]

    return cfg



def save_settings(cfg):
    save_json(SETTINGS_PATH, cfg)



def load_wifi():
    cfg = load_json(WIFI_PATH, {})

    if not isinstance(cfg, dict):
        return {}

    return cfg



def save_wifi(cfg):
    save_json(WIFI_PATH, cfg)
