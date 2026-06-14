print("[IMPORT] weather")

import time
import graphics as g
import system

exec(open("/flash/apps/weather/weather_api.py").read())
exec(open("/flash/apps/weather/weather_ui.py").read())

print("[APP] graphics.init()")
g.init()

AUTO_REFRESH_MS = 10 * 60 * 1000

PAGE_CURRENT = 0
PAGE_HOURLY = 1
PAGE_DAILY = 2
PAGE_SUN = 3

page = PAGE_CURRENT

last_refresh = 0
last_draw = -1

print("[APP] Loading weather")

data = get_weather()

location = data["location"]
weather = data["weather"]


def refresh_weather():

    global data
    global location
    global weather
    global last_refresh

    print("[APP] Refreshing weather")

    try:

        data = get_weather()

        location = data["location"]
        weather = data["weather"]

        last_refresh = time.ticks_ms()

        print("[APP] Refresh success")

        return True

    except Exception as e:

        print(
            "[APP] Refresh failed:",
            e
        )

        return False


def redraw():

    global page

    print(
        "[APP] Redraw page",
        page
    )

    if "error" in weather:

        draw_error(
            weather["error"]
        )

        return

    desc = weather_desc(
        weather["current"]["code"]
    )

    icon = weather_icon(
        weather["current"]["code"]
    )

    if page == PAGE_CURRENT:

        draw_current(
            weather,
            location,
            desc,
            icon
        )

    elif page == PAGE_HOURLY:

        draw_hourly(
            weather
        )

    elif page == PAGE_DAILY:

        draw_daily(
            weather,
            weather_desc
        )

    elif page == PAGE_SUN:

        draw_sun(
            weather
        )


def next_page():

    global page

    page += 1

    if page > PAGE_SUN:

        page = PAGE_CURRENT

    print(
        "[APP] Page ->",
        page
    )


def key1_held(ms=1200):

    start = time.ticks_ms()

    while system.key1_pressed():

        if (
            time.ticks_diff(
                time.ticks_ms(),
                start
            ) > ms
        ):

            return True

        time.sleep_ms(20)

    return False


print("[APP] First draw")

redraw()

while True:

    try:

        # --------------------
        # K1
        # --------------------

        if system.key1_just_pressed():

            print(
                "[INPUT] K1 pressed"
            )

            time.sleep_ms(50)

            if key1_held():

                print(
                    "[INPUT] K1 hold"
                )

                refresh_weather()

                redraw()

            else:

                next_page()

                redraw()

        # --------------------
        # K2
        # --------------------

        if system.key2_just_pressed():

            print(
                "[INPUT] K2 exit"
            )

            break

        # --------------------
        # AUTO REFRESH
        # --------------------

        now = time.ticks_ms()

        if (
            time.ticks_diff(
                now,
                last_refresh
            )
            >
            AUTO_REFRESH_MS
        ):

            print(
                "[AUTO] Refresh"
            )

            refresh_weather()

            redraw()

        time.sleep_ms(50)

    except Exception as e:

        print(
            "[APP] Main loop error:",
            e
        )

        try:

            draw_error(str(e))

        except:

            pass

        time.sleep(1)

print("[APP] Exit")