import time, random, system, graphics as g

g.init()
c = g.canvas

WIDTH, HEIGHT = 240, 135

STATE_WAIT = 0
STATE_READY = 1
STATE_GO = 2

state = STATE_WAIT
start_time = 0
wait_time = 0
result = ""

exit_hold_start = None

def check_exit():
    global exit_hold_start

    if system.key1_pressed() and system.key2_pressed():

        if exit_hold_start is None:
            exit_hold_start = time.ticks_ms()

        elif time.ticks_diff(time.ticks_ms(), exit_hold_start) > 2000:
            return True

    else:
        exit_hold_start = None

    return False

while True:

    if check_exit():
        break

    if state == STATE_WAIT:
        c.fillScreen(0x000000)
        c.setCursor(10, 60)
        c.print("Press K1 to start")

        if system.key1_just_pressed():
            wait_time = random.randint(1000, 4000)
            start_time = time.ticks_ms()
            state = STATE_READY

    elif state == STATE_READY:
        c.fillScreen(0x222200)
        c.setCursor(10, 60)
        c.print("WAIT...")

        if time.ticks_diff(time.ticks_ms(), start_time) > wait_time:
            state = STATE_GO
            start_time = time.ticks_ms()

    elif state == STATE_GO:
        c.fillScreen(0x002200)
        c.setCursor(10, 60)
        c.print("GO!")

        if system.key1_just_pressed():
            rt = time.ticks_diff(time.ticks_ms(), start_time)
            result = str(rt) + " ms"
            state = STATE_WAIT

    if result:
        c.setCursor(10, 90)
        c.print(result)

    c.push(0, 0)
    time.sleep_ms(30)