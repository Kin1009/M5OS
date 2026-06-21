import math
import random
import system
import time

from M5 import Power

import config_store

import graphics as g

import wifi_manager


g.init()
canvas = g.canvas

apps_menu = 0
power_menu = 0

WIDTH = 240
HEIGHT = 135

BLACK = 0x000000
TOPBAR_BG = 0x111111
WHITE = 0xFFFFFF

TOPBAR_H = 16


# -------------------------
# PARTICLES (3x3 = 9 DOTS)
# -------------------------

N = 20
RADIUS = 3
collisions = 0
dots = []
wifi_anim_timer = 0
wifi_anim_frame = 1
wifi_blink = False
for i in range(N):

    dots.append({
        "x": random.randint(20, WIDTH - 20),
        "y": random.randint(20, HEIGHT - 20),
        "vx": random.uniform(-4, 4),
        "vy": random.uniform(-4, 4),
    })

# -------------------------
# UPDATE PHYSICS
# -------------------------

def wifi_icon():

    global wifi_anim_timer
    global wifi_anim_frame
    global wifi_blink

    state = wifi_manager.status()

    # -------------------------
    # DISCONNECTED (BLINK wifi-0)
    # -------------------------
    if state in ('OFF', 'FAIL', 'ERROR', 'DISCONNECTED'):

        wifi_anim_timer += 1

        # blink every ~10 frames
        if wifi_anim_timer % 10 == 0:
            wifi_blink = not wifi_blink

        if wifi_blink:
            return '/flash/apps/startup/wifi-0.bmp'
        else:
            return None  # draw nothing (blink off)


    # -------------------------
    # CONNECTING (ANIMATE 1 TO 3)
    # -------------------------
    if state == "CONNECTING":

        wifi_anim_timer += 1

        # slow animation speed
        if wifi_anim_timer % 6 == 0:
            wifi_anim_frame += 1
            if wifi_anim_frame > 3:
                wifi_anim_frame = 1

        return '/flash/apps/startup/wifi-%d.bmp' % wifi_anim_frame


    # -------------------------
    # CONNECTED (STABLE FULL)
    # -------------------------
    if state == "CONNECTED":
        return '/flash/apps/startup/wifi-3.bmp'

    return '/flash/apps/startup/wifi-0.bmp'

def update_dots():
    global collisions
    for i in range(N):

        d = dots[i]

        # move
        d['x'] += d['vx']
        d['y'] += d['vy']

        # wall bounce
        if d['x'] < RADIUS:
            d['x'] = RADIUS
            d['vx'] *= -1

        if d['x'] > WIDTH - RADIUS:
            d['x'] = WIDTH - RADIUS
            d['vx'] *= -1

        if d['y'] < TOPBAR_H + RADIUS:
            d['y'] = TOPBAR_H + RADIUS
            d['vy'] *= -1

        if d['y'] > HEIGHT - RADIUS:
            d['y'] = HEIGHT - RADIUS
            d['vy'] *= -1

    # -------------------------
    # DOT-DOT COLLISION
    # -------------------------

    for i in range(N):
        for j in range(i + 1, N):

            a = dots[i]
            b = dots[j]

            dx = b['x'] - a['x']
            dy = b['y'] - a['y']

            dist = math.sqrt(dx * dx + dy * dy)

            min_dist = RADIUS * 2

            if dist < min_dist and dist > 0:

                # normalize
                nx = dx / dist
                ny = dy / dist

                # push apart (separate overlap)
                overlap = min_dist - dist

                a['x'] -= nx * overlap * 0.5
                a['y'] -= ny * overlap * 0.5
                b['x'] += nx * overlap * 0.5
                b['y'] += ny * overlap * 0.5

                # swap velocity components (elastic-ish bounce)
                a['vx'], b['vx'] = b['vx'], a['vx']
                a['vy'], b['vy'] = b['vy'], a['vy']
                collisions += 1


# -------------------------
# DRAW
# -------------------------


def draw_dots():

    for d in dots:

        x = int(d['x'])
        y = int(d['y'])

        canvas.fillCircle(x, y, RADIUS, 0x555555)

# -------------------------
# LOAD SETTINGS
# -------------------------

settings = config_store.load_settings()


def battery_icon():

    try:
        if Power.isCharging():
            return '/flash/apps/startup/bat-charge.bmp'

        lvl = system.battery_level()

        # clamp 0-100
        if lvl < 0:
            lvl = 0
        elif lvl > 100:
            lvl = 100

        # map to 4 levels
        if lvl <= 25:
            return '/flash/apps/startup/bat-1.bmp'
        elif lvl <= 50:
            return '/flash/apps/startup/bat-2.bmp'
        elif lvl <= 75:
            return '/flash/apps/startup/bat-3.bmp'
        else:
            return '/flash/apps/startup/bat-4.bmp'

    except:
        return '/flash/apps/startup/bat-1.bmp'
# -------------------------
# WIFI INIT
# -------------------------
need_restart = 1
if settings.get('autowifi', 1):
    need_restart = 0
    wifi_manager.start()

# -------------------------
# MAIN LOOP
# -------------------------
while True:
    if (system._wifi_state == 
        'CONNECTED' and time.time() - system._last_ntp_sync > 86400):
        system.ntp_sync()
    if not settings.get('autowifi', 1):
        need_restart = 1
    # -------------------------
    # WIFI UPDATE (ONLY ONE PATH)
    # -------------------------

    if settings.get('autowifi', 1):
        if need_restart:
            need_restart = 0
            wifi_manager.start()
        system.wifi_update()
        wifi_manager.update()

    # -------------------------
    # CLEAR
    # -------------------------

    canvas.fillScreen(BLACK)

    # -------------------------
    # PHYSICS
    # -------------------------

    update_dots()
    draw_dots()

    # -------------------------
    # TOP BAR
    # -------------------------

    canvas.fillRect(0, 0, WIDTH, TOPBAR_H, TOPBAR_BG)

    # Time
    canvas.setTextColor(WHITE, TOPBAR_BG)
    canvas.setCursor(20, 1)
    canvas.print(system.time_label())

    # -------------------------
    # WIFI STATUS
    # -------------------------

    icon = wifi_icon()

    if icon is not None:
        canvas.drawImage(
            icon,
            2,
            1,
            16,
            16,
            1, 1, 1, 1
        )
    # ------------------------
    # -
    # BATTERY
    # -------------------------

    batt = str(system.battery_level()) + '%'

    canvas.setCursor(WIDTH - len(batt) * 8 - 3, 1)
    canvas.print(batt)

    icon = battery_icon()

    canvas.drawImage(
        icon,
        WIDTH - len(batt) * 8 - 18,
        1,
        16,
        16,
        1, 1, 1, 1
    )

    # -------------------------
    # DEBUG
    # -------------------------

    canvas.setTextColor(WHITE, BLACK)
    canvas.setCursor(2, 18)
    canvas.print("Collisions: " + str(collisions))

    canvas.push(0, 0)

    # -------------------------
    # INPUT
    # -------------------------

    if system.key1_just_pressed():

        system.safe_run_app('/flash/apps/apps/apps.py')

    elif system.key2_just_pressed():

        system.safe_run_app('/flash/apps/power/power.py')

    # -------------------------
    # FRAME LIMIT
    # -------------------------

    # time.sleep_ms(40)
