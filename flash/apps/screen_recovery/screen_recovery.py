import time, random, system, graphics as g

g.init()
c = g.canvas

W, H = 240, 135

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

    for y in range(0, H, 4):
        for x in range(0, W, 4):

            c.fillRect(
                x,
                y,
                4,
                4,
                random.randint(0, 0xFFFFFF)
            )
    c.push(0, 0)