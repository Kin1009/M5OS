print("[IMPORT] weather_api")

import json
import os
import time
import urequests as requests

CACHE_FILE = "/flash/apps/weather/cache.json"
LOCATION_FILE = "/flash/apps/weather/location.json"

ICON_SUN = "/flash/apps/weather/sun.bmp"
ICON_CLOUD = "/flash/apps/weather/cloud.bmp"
ICON_RAIN = "/flash/apps/weather/rain.bmp"

DEFAULT_LOCATION = {
    "lat": 12.2388,
    "lon": 109.1967,
    "city": "Nha Trang"
}


def load_json(path):

    print("[JSON] Load:", path)

    try:

        with open(path, "r") as f:

            return json.load(f)

    except Exception as e:

        print("[JSON] Failed:", e)

        return None


def save_json(path, data):

    print("[JSON] Save:", path)

    try:

        with open(path, "w") as f:

            json.dump(data, f)

        return True

    except Exception as e:

        print("[JSON] Failed:", e)

        return False


def weather_desc(code):

    if code == 0:
        return "Clear"

    elif code <= 3:
        return "Partly Cloudy"

    elif code in (51, 53, 55):
        return "Drizzle"

    elif code in (61, 63, 65):
        return "Rain"

    elif code in (80, 81, 82):
        return "Rain Showers"

    elif code == 95:
        return "Thunderstorm"

    return "Unknown"


def weather_icon(code):

    if code == 0:
        return ICON_SUN

    elif code <= 3:
        return ICON_CLOUD

    return ICON_RAIN


def load_location():

    print("[LOCATION] Loading cached location")

    loc = load_json(LOCATION_FILE)

    if loc:

        print("[LOCATION] Cache hit")

        return loc

    print("[LOCATION] Using default")

    return DEFAULT_LOCATION.copy()


def fetch_location():

    print("[LOCATION] Fetching from ip-api")

    try:

        r = requests.get(
            "http://ip-api.com/json"
        )

        data = r.json()

        r.close()

        loc = {
            "lat": data.get("lat", 1.35),
            "lon": data.get("lon", 103.82),
            "city": data.get("city", "Unknown")
        }

        print("[LOCATION] Success:", loc)

        save_json(
            LOCATION_FILE,
            loc
        )

        return loc

    except Exception as e:

        print("[LOCATION] Failed:", e)

        return load_location()


def load_cache():

    print("[CACHE] Loading")

    return load_json(CACHE_FILE)


def save_cache(data):

    print("[CACHE] Saving")

    save_json(
        CACHE_FILE,
        {
            "timestamp": time.time(),
            "data": data
        }
    )


def fetch_weather(lat, lon):

    print("[WEATHER] Fetching")

    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=" + str(lat) +
        "&longitude=" + str(lon) +
        "&current="
        "temperature_2m,"
        "apparent_temperature,"
        "relative_humidity_2m,"
        "weather_code,"
        "wind_speed_10m,"
        "precipitation"
        "&hourly="
        "temperature_2m,"
        "precipitation_probability,"
        "weather_code"
        "&daily="
        "weather_code,"
        "temperature_2m_max,"
        "temperature_2m_min,"
        "sunrise,"
        "sunset"
        "&forecast_days=3"
        "&timezone=auto"
    )

    last_err = None

    for attempt in range(3):

        print(
            "[WEATHER] Attempt",
            attempt + 1
        )

        try:

            r = requests.get(url)

            data = r.json()

            r.close()

            current = data["current"]

            result = {

                "timezone":
                    data.get(
                        "timezone",
                        "Unknown"
                    ),

                "current": {

                    "temp":
                        current[
                            "temperature_2m"
                        ],

                    "feels":
                        current[
                            "apparent_temperature"
                        ],

                    "humidity":
                        current[
                            "relative_humidity_2m"
                        ],

                    "wind":
                        current[
                            "wind_speed_10m"
                        ],

                    "rain":
                        current[
                            "precipitation"
                        ],

                    "code":
                        current[
                            "weather_code"
                        ]
                },

                "hourly":
                    data["hourly"],

                "daily":
                    data["daily"]
            }

            print(
                "[WEATHER] Success"
            )

            save_cache(result)

            return result

        except Exception as e:

            last_err = str(e)

            print(
                "[WEATHER] Failed:",
                e
            )

            time.sleep(1)

    print(
        "[WEATHER] Using cache"
    )

    cache = load_cache()

    if cache:

        return cache["data"]

    return {
        "error": last_err
    }


def get_weather():

    print(
        "[WEATHER] get_weather()"
    )

    location = fetch_location()

    weather = fetch_weather(
        location["lat"],
        location["lon"]
    )

    return {
        "location": location,
        "weather": weather
    }