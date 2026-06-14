print("[IMPORT] weather_ui")

import graphics as g

canvas = g.canvas

# -------------------------
# COLORS
# -------------------------

BG = 0x0B0F14
CARD = 0x111826

WHITE = 0xFFFFFF
GREY = 0x9AA4B2

BLUE = 0x60A5FA
GREEN = 0x22C55E
YELLOW = 0xFACC15
RED = 0xEF4444

# -------------------------
# HELPERS
# -------------------------

def clear():

    canvas.fillScreen(BG)


def topbar(title):

    canvas.fillRect(
        0,
        0,
        240,
        18,
        CARD
    )

    canvas.setTextColor(
        WHITE,
        CARD
    )

    canvas.drawString(
        str(title),
        5,
        4
    )


def footer(text):

    canvas.fillRect(
        0,
        120,
        240,
        15,
        CARD
    )

    canvas.setTextColor(
        GREY,
        CARD
    )

    canvas.drawString(
        text,
        5,
        123
    )


def push():

    canvas.push(
        0,
        0
    )


def short_time(timestr):

    try:

        return timestr.split("T")[1]

    except:

        return "--:--"


# -------------------------
# CURRENT WEATHER PAGE
# -------------------------

def draw_current(
    weather,
    location,
    desc,
    icon_path
):

    print("[UI] draw_current")

    clear()

    city = location.get(
        "city",
        "Unknown"
    )

    topbar(city)

    try:

        canvas.drawImage(
            icon_path,
            10,
            28
        )

    except Exception as e:

        print(
            "[UI] icon failed:",
            e
        )

    current = weather["current"]

    canvas.setTextColor(
        WHITE,
        BG
    )

    canvas.setTextSize(2)

    canvas.drawString(
        str(
            round(
                current["temp"]
            )
        ) + "C",
        80,
        28
    )

    canvas.setTextSize(1)

    canvas.setTextColor(
        GREY,
        BG
    )

    canvas.drawString(
        "Feels "
        + str(
            round(
                current["feels"]
            )
        )
        + "C",
        80,
        55
    )

    canvas.setTextColor(
        WHITE,
        BG
    )

    canvas.drawString(
        desc,
        10,
        80
    )

    canvas.setTextColor(
        BLUE,
        BG
    )

    canvas.drawString(
        "Hum "
        + str(
            current["humidity"]
        )
        + "%",
        10,
        100
    )

    canvas.setTextColor(
        GREEN,
        BG
    )

    canvas.drawString(
        "Wind "
        + str(
            round(
                current["wind"]
            )
        )
        + "km/h",
        90,
        100
    )

    canvas.setTextColor(
        YELLOW,
        BG
    )

    canvas.drawString(
        "Rain "
        + str(
            current["rain"]
        ),
        170,
        100
    )

    footer(
        "K1 Next  Hold K1 Refresh  K2 Exit"
    )

    push()


# -------------------------
# HOURLY PAGE
# -------------------------

def draw_hourly(weather):

    print("[UI] draw_hourly")

    clear()

    topbar(
        "Next 6 Hours"
    )

    hourly = weather["hourly"]

    temps = hourly[
        "temperature_2m"
    ]

    rain = hourly[
        "precipitation_probability"
    ]

    times = hourly[
        "time"
    ]

    start = 0

    for i in range(6):

        x = (
            i * 38
        ) + 5

        try:

            t = short_time(
                times[
                    start + i
                ]
            )

            temp = str(
                round(
                    temps[
                        start + i
                    ]
                )
            )

            r = str(
                rain[
                    start + i
                ]
            )

        except:

            continue

        canvas.setTextColor(
            GREY,
            BG
        )

        canvas.drawString(
            t,
            x,
            30
        )

        canvas.setTextColor(
            WHITE,
            BG
        )

        canvas.drawString(
            temp + "C",
            x,
            55
        )

        if int(r) >= 70:

            color = RED

        elif int(r) >= 40:

            color = YELLOW

        else:

            color = GREEN

        canvas.setTextColor(
            color,
            BG
        )

        canvas.drawString(
            r + "%",
            x,
            80
        )

    footer(
        "Page 2/4"
    )

    push()


# -------------------------
# 3 DAY FORECAST
# -------------------------

def draw_daily(
    weather,
    desc_func
):

    print("[UI] draw_daily")

    clear()

    topbar(
        "3 Day Forecast"
    )

    daily = weather[
        "daily"
    ]

    for i in range(3):

        y = (
            i * 30
        ) + 25

        try:

            day = daily[
                "time"
            ][i]

            max_t = daily[
                "temperature_2m_max"
            ][i]

            min_t = daily[
                "temperature_2m_min"
            ][i]

            code = daily[
                "weather_code"
            ][i]

        except:

            continue

        canvas.setTextColor(
            WHITE,
            BG
        )

        canvas.drawString(
            day,
            5,
            y
        )

        canvas.drawRightString(
            str(
                round(
                    max_t
                )
            )
            + "/"
            + str(
                round(
                    min_t
                )
            ),
            235,
            y
        )

        canvas.setTextColor(
            GREY,
            BG
        )

        canvas.drawString(
            desc_func(code),
            5,
            y + 12
        )

    footer(
        "Page 3/4"
    )

    push()


# -------------------------
# SUN PAGE
# -------------------------

def draw_sun(weather):

    print("[UI] draw_sun")

    clear()

    topbar(
        "Sun Info"
    )

    daily = weather[
        "daily"
    ]

    sunrise = short_time(
        daily[
            "sunrise"
        ][0]
    )

    sunset = short_time(
        daily[
            "sunset"
        ][0]
    )

    canvas.setTextColor(
        YELLOW,
        BG
    )

    canvas.drawString(
        "Sunrise",
        20,
        35
    )

    canvas.drawString(
        sunrise,
        20,
        55
    )

    canvas.drawString(
        "Sunset",
        140,
        35
    )

    canvas.drawString(
        sunset,
        140,
        55
    )

    canvas.setTextColor(
        GREY,
        BG
    )

    canvas.drawString(
        weather.get(
            "timezone",
            "Unknown"
        ),
        20,
        95
    )

    footer(
        "Page 4/4"
    )

    push()


# -------------------------
# ERROR PAGE
# -------------------------

def draw_error(err):

    print("[UI] draw_error")

    clear()

    topbar(
        "Weather Error"
    )

    canvas.setTextColor(
        RED,
        BG
    )

    canvas.drawString(
        str(err),
        5,
        40
    )

    footer(
        "K2 Exit"
    )

    push()