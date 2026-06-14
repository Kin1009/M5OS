import graphics as g
import system

g.init()

while True:

    scene = [

        g.Text(
            "Hello World",
            0xFFFFFF,
            84,
            64
        )

    ]

    g.update(scene)
    g.render()

    if (
        system.key1_just_pressed()
        or
        system.key2_just_pressed()
    ):
        break