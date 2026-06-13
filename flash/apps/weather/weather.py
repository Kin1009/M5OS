import urequests as requests
import time
import system
import graphics as g

# -------------------------
# COLORS
# -------------------------
BG = 0x0B0F14
CARD = 0x111826
WHITE = 0xFFFFFF
GREY = 0x9AA4B2
RED = 0xEF4444

# -------------------------
# ICONS
# -------------------------
ICON_SUN = "/flash/apps/weather/sun.bmp"
ICON_CLOUD = "/flash/apps/weather/cloud.bmp"
ICON_RAIN = "/flash/apps/weather/rain.bmp"


# -------------------------
# AUTO LOCATION
# -------------------------
def get_location():

    try:
        r = requests.get("http://ip-api.com/json")
        data = r.json()
        r.close()

        return {
            "lat": data.get("lat", 1.35),
            "lon": data.get("lon", 103.82),
            "city": data.get("city", "Unknown")
        }

    except Exception as e:

        return {
            "lat": 1.35,
            "lon": 103.82,
            "city": "Offline",
            "error": str(e)
        }


# -------------------------
# SAFE WEATHER FETCH
# -------------------------
def fetch_weather(lat, lon):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=" + str(lat) +
        "&longitude=" + str(lon) +
        "&current_weather=true"
    )

    # retry system (VERY IMPORTANT on ESP32)
    for attempt in range(3):

        try:
            r = requests.get(url)
            data = r.json()
            r.close()

            w = data.get("current_weather")

            if not w:
                return {"error": "No weather data"}

            return {
                "temp": w.get("temperature", "--"),
                "wind": w.get("windspeed", "--"),
                "code": w.get("weathercode", -1)
            }

        except Exception as e:
            time.sleep(0.5)

            last_err = str(e)

    return {"error": last_err}


# -------------------------
# ICON MAP
# -------------------------
def get_icon(code):

    if code == 0:
        return ICON_SUN
    elif 1 <= code <= 3:
        return ICON_CLOUD
    else:
        return ICON_RAIN


# -------------------------
# DRAW UI
# -------------------------
def draw(weather, location):

    c = g.canvas
    c.fillScreen(BG)

    # top bar
    c.fillRect(0, 0, 240, 18, CARD)

    c.setTextColor(GREY, CARD)
    c.setCursor(4, 4)
    c.print(location.get("city", "Unknown"))

    # main card
    c.fillRect(10, 25, 220, 100, CARD)

    # error handling
    if "error" in weather:

        c.setTextColor(RED, CARD)
        c.setCursor(20, 60)
        c.print("Weather error")

        c.setCursor(20, 80)
        c.print(str(weather["error"])[:30])

    else:

        try:
            c.drawImage(get_icon(weather["code"]), 20, 35)
        except:
            pass

        c.setTextColor(WHITE, CARD)
        c.setCursor(90, 50)
        c.print(str(weather["temp"]) + " C")

        c.setTextColor(GREY, CARD)
        c.setCursor(90, 75)
        c.print("Wind: " + str(weather["wind"]))


    # footer
    c.setCursor(10, 140)
    c.setTextColor(GREY, BG)
    c.print("K1 refresh  K2 exit")

    c.push(0, 0)


# -------------------------
# APP
# -------------------------
def weather_app():

    location = get_location()
    weather = fetch_weather(location["lat"], location["lon"])

    last_refresh = 0

    while True:

        # refresh button (debounced)
        if system.key1_just_pressed():
            weather = fetch_weather(location["lat"], location["lon"])
            last_refresh = time.ticks_ms()

        if system.key2_just_pressed():
            return

        # auto refresh every 60s
        if time.ticks_ms() - last_refresh > 60000:
            weather = fetch_weather(location["lat"], location["lon"])
            last_refresh = time.ticks_ms()

        draw(weather, location)
        time.sleep_ms(300)


weather_app()