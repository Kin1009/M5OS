import time
import random
import system
import graphics as g

g.init()
canvas = g.canvas

WIDTH = 240
HEIGHT = 135

BLACK = 0x000000
WHITE = 0xFFFFFF

# -------------------------
# SETTINGS
# -------------------------

PADDLE_X = 5
PADDLE_W = 5
PADDLE_H = 25

BALL_R = 3

lp_y = HEIGHT // 2
rp_y = HEIGHT // 2

ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_vx = 3
ball_vy = 2

score_l = 0
score_r = 0

hold_start = None

speed_mul = 1.0

# trail buffer (store previous positions)
trail = []


# -------------------------
# RESET BALL
# -------------------------

def reset_ball(direction=1):
    global ball_x, ball_y, ball_vx, ball_vy, speed_mul, trail

    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2

    speed_mul = 1.0

    ball_vx = 3 * direction
    ball_vy = random.choice([-2, -1, 1, 2])

    trail = []


# -------------------------
# MAIN LOOP
# -------------------------

while True:

    # -------------------------
    # INPUT
    # -------------------------
    if system.key1_pressed() and not system.key2_pressed():
        lp_y += 4
    elif system.key2_pressed() and not system.key1_pressed():
        lp_y -= 4

    if lp_y < PADDLE_H // 2:
        lp_y = PADDLE_H // 2
    if lp_y > HEIGHT - PADDLE_H // 2:
        lp_y = HEIGHT - PADDLE_H // 2


    # -------------------------
    # EXIT HOLD
    # -------------------------
    if system.key1_pressed() and system.key2_pressed():
        if hold_start is None:
            hold_start = time.ticks_ms()
        elif time.ticks_diff(time.ticks_ms(), hold_start) > 2000:
            break
    else:
        hold_start = None


    # -------------------------
    # AI PADDLE
    # -------------------------
    if ball_y > rp_y:
        rp_y += 3
    else:
        rp_y -= 3

    if rp_y < PADDLE_H // 2:
        rp_y = PADDLE_H // 2
    if rp_y > HEIGHT - PADDLE_H // 2:
        rp_y = HEIGHT - PADDLE_H // 2


    # -------------------------
    # TRAIL SAVE
    # -------------------------
    trail.append((ball_x, ball_y))
    if len(trail) > 12:
        trail.pop(0)


    # -------------------------
    # BALL UPDATE
    # -------------------------
    ball_x += ball_vx * speed_mul
    ball_y += ball_vy * speed_mul

    # speed increase over time
    speed_mul *= 1.002
    if speed_mul > 3.0:
        speed_mul = 3.0


    # top/bottom bounce
    if ball_y <= 0 or ball_y >= HEIGHT:
        ball_vy *= -1


    # -------------------------
    # LEFT PADDLE COLLISION + SPIN
    # -------------------------
    if ball_x <= PADDLE_X + PADDLE_W:

        if abs(ball_y - lp_y) < PADDLE_H // 2:

            # spin effect
            offset = (ball_y - lp_y) / (PADDLE_H / 2)
            ball_vy += offset * 2

            ball_vx *= -1

            speed_mul *= 1.05

        else:
            score_r += 1
            reset_ball(1)


    # -------------------------
    # RIGHT PADDLE COLLISION + SPIN
    # -------------------------
    if ball_x >= WIDTH - PADDLE_X - PADDLE_W:

        if abs(ball_y - rp_y) < PADDLE_H // 2:

            offset = (ball_y - rp_y) / (PADDLE_H / 2)
            ball_vy += offset * 2

            ball_vx *= -1

            speed_mul *= 1.05

        else:
            score_l += 1
            reset_ball(-1)


    # -------------------------
    # DRAW (TRAIL EFFECT)
    # -------------------------
    canvas.fillScreen(BLACK)

    # trail (fade style)
    for i, p in enumerate(trail):
        x, y = p
        c = 40 + i * 15
        color = (c << 16) | (c << 8) | c  # gray fade
        canvas.fillCircle(int(x), int(y), BALL_R, color)

    # paddles
    canvas.fillRect(PADDLE_X, lp_y - PADDLE_H // 2, PADDLE_W, PADDLE_H, WHITE)
    canvas.fillRect(WIDTH - PADDLE_X - PADDLE_W, rp_y - PADDLE_H // 2, PADDLE_W, PADDLE_H, WHITE)

    # ball (bright)
    canvas.fillCircle(int(ball_x), int(ball_y), BALL_R, WHITE)

    # score
    canvas.setCursor(40, 5)
    canvas.print(str(score_l))

    canvas.setCursor(WIDTH - 40, 5)
    canvas.print(str(score_r))

    canvas.push(0, 0)

    time.sleep_ms(16)