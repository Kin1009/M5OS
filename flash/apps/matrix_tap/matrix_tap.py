import time, random, system, graphics as g

g.init()
c = g.canvas

W, H = 240, 135

x = random.randint(0, W-1)
y = random.randint(16, H-1)

score = 0

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

    if system.key1_just_pressed():
        if abs(x - 120) < 30:
            score += 1
        x = random.randint(0, W-1)
        y = random.randint(16, H-1)

    if system.key2_just_pressed():
        if abs(y - 67) < 30:
            score += 1
        x = random.randint(0, W-1)
        y = random.randint(16, H-1)

    c.fillScreen(0x000000)

    c.fillRect(x, y, 3, 3, 0xFFFFFF)

    c.setCursor(5, 5)
    c.print("Score: " + str(score))

    c.push(0, 0)
    time.sleep_ms(30)