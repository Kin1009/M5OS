import graphics as g
import system
import time

g.init()
canvas = g.canvas

WIDTH = 240
HEIGHT = 135

BLACK = 0x000000
WHITE = 0xFFFFFF
GRAY = 0x444444
DARK = 0x111111

# -------------------------
# GRID
# -------------------------
ROWS = 4
COLS = 4

BTN_W = WIDTH // COLS
BTN_H = (HEIGHT - 40) // ROWS

grid = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "x"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"],
]

cx = 0
cy = 0

expr = ""
result = ""

exit_start = None
# -------------------------
# COMPUTE
# -------------------------
def compute(e):
    try:
        return str(eval(e))
    except:
        return "ERR"


# -------------------------
# DRAW
# -------------------------
def draw():

    canvas.fillScreen(BLACK)

    # display
    canvas.fillRect(5, 5, 230, 30, DARK)
    canvas.drawRect(5, 5, 230, 30, WHITE)

    canvas.setTextColor(WHITE, DARK)
    canvas.setCursor(10, 15)

    if result:
        canvas.print(result)
    else:
        canvas.print(expr)

    # grid
    for y in range(ROWS):
        for x in range(COLS):

            bx = x * BTN_W
            by = 40 + y * BTN_H

            val = grid[y][x]

            selected = (x == cx and y == cy)
            bg = GRAY if selected else DARK

            canvas.fillRect(bx + 1, by + 1, BTN_W - 2, BTN_H - 2, bg)
            canvas.drawRect(bx + 1, by + 1, BTN_W - 2, BTN_H - 2, WHITE)

            # text shifted up (-3)
            canvas.setTextColor(WHITE, bg)
            canvas.setCursor(bx + BTN_W // 2 - 4, by + BTN_H // 2 - 7)

            canvas.print(val)

    canvas.push(0, 0)

run = 1
# -------------------------
# INPUT
# -------------------------
def handle_input():

    global cx, cy, expr, result
    global exit_start, run

    # -------------------------
    # HOLD K1 + K2 TO EXIT
    # -------------------------
    if system.key1_pressed() and system.key2_pressed():

        if exit_start is None:
            exit_start = time.ticks_ms()

        else:
            if time.ticks_diff(time.ticks_ms(), exit_start) > 2000:
                run = 0
                return

    else:
        exit_start = None
    # K2 = switch cell
    if system.key2_just_pressed():
        cx += 1
        if cx >= COLS:
            cx = 0
            cy += 1
            if cy >= ROWS:
                cy = 0

    # K1 = select
    if system.key1_just_pressed():

        val = grid[cy][cx]

        if val == "C":
            expr = ""
            result = ""

        elif val == "=":
            result = compute(expr.replace("x", "*").replace("÷", "/"))

        else:
            if result:
                expr = result
                result = ""

            expr += val


# -------------------------
# MAIN LOOP
# -------------------------
while run:
    
    handle_input()
    draw()

    time.sleep_ms(40)