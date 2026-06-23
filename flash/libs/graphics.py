import M5

from M5 import *


print("[debug] graphics module loaded")

canvas = None

system_scene = []
user_scene = []


# -------------------------
# INIT
# -------------------------

def init():
    global canvas

    print("[debug] graphics.init")

    M5.begin()

    print("[debug] set rotation")
    Widgets.setRotation(1)

    print("[debug] clear screen")
    Widgets.fillScreen(0x000000)

    print("[debug] create canvas 240x135")
    canvas = M5.Lcd.newCanvas(
        240,
        135,
        16,
        True
    )

    print("[debug] set font")
    canvas.setFont(
        Widgets.FONTS.Montserrat12
    )

    print("[debug] graphics.init complete")


# -------------------------
# UPDATE PHASE
# -------------------------

def update_system(new_list):
    """
    Replace system objects list
    """
    global system_scene

    print(
        "[debug] update_system objects =",
        len(new_list)
    )

    system_scene = new_list


def update(new_list):
    """
    Replace user objects list
    """
    global user_scene

    print(
        "[debug] update objects =",
        len(new_list)
    )

    user_scene = new_list


# -------------------------
# RENDER PHASE
# -------------------------

def flatten(scene):
    """
    Converts nested lists into flat list of drawable objects
    """
    result = []

    for item in scene:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)

    return result


def render(bg=0x000000):
    global canvas

    if canvas is None:
        print("[debug] render called before init")
        return

    canvas.fillScreen(bg)

    flat_system = flatten(system_scene)
    flat_user = flatten(user_scene)

    print(
        "[debug] render system=%d user=%d"
        % (
            len(flat_system),
            len(flat_user)
        )
    )

    # system layer
    for obj in flat_system:
        try:
            obj.draw(canvas)
        except Exception as e:
            print(
                "[debug] system draw failed:",
                e
            )

    # user layer
    for obj in flat_user:
        try:
            obj.draw(canvas)
        except Exception as e:
            print(
                "[debug] user draw failed:",
                e
            )

    canvas.push(0, 0)


class UIObject:
    def draw(self, canvas):
        pass


class Text(UIObject):
    def __init__(
        self,
        text,
        fg,
        x,
        y,
        bg=None
    ):
        print(
            "[debug] Text",
            repr(text),
            "@",
            x,
            y
        )

        self.text = text
        self.fg = fg
        self.bg = bg
        self.x = x
        self.y = y

    def draw(self, c):
        c.setCursor(
            self.x,
            self.y
        )

        if self.bg is not None:
            c.setTextColor(
                self.fg,
                self.bg
            )
        else:
            c.setTextColor(
                self.fg
            )

        c.print(self.text)


class Rectangle(UIObject):
    def __init__(
        self,
        color,
        x,
        y,
        w,
        h
    ):
        print(
            "[debug] Rectangle",
            x,
            y,
            w,
            h
        )

        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, c):
        c.fillRect(
            self.x,
            self.y,
            self.w,
            self.h,
            self.color
        )


class Circle(UIObject):
    def __init__(
        self,
        color,
        x,
        y,
        r
    ):
        print(
            "[debug] Circle",
            x,
            y,
            r
        )

        self.color = color
        self.x = x
        self.y = y
        self.r = r

    def draw(self, c):
        c.fillCircle(
            self.x,
            self.y,
            self.r,
            self.color
        )


class Line(UIObject):
    def __init__(
        self,
        color,
        x1,
        y1,
        x2,
        y2
    ):
        print(
            "[debug] Line",
            x1,
            y1,
            x2,
            y2
        )

        self.color = color
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, c):
        c.drawLine(
            self.x1,
            self.y1,
            self.x2,
            self.y2,
            self.color
        )


class BorderedRectangle(UIObject):
    def __init__(
        self,
        x,
        y,
        w,
        h,
        border_color,
        fill_color
    ):
        print(
            "[debug] BorderedRectangle",
            x,
            y,
            w,
            h
        )

        self.border = Rectangle(
            border_color,
            x,
            y,
            w,
            h
        )

        self.fill = Rectangle(
            fill_color,
            x + 1,
            y + 1,
            w - 2,
            h - 2
        )

    def draw(self, c):
        self.fill.draw(c)
        self.border.draw(c)


print("[debug] graphics module ready")