from M5 import Power
import M5

import machine

import ui



def power_menu():

    choice = ui.chooser(
        [
            'Restart',
            "Power off",
            "Download mode",
            'Return'
        ],
        label="Power Menu"
    )

    # -------------------------
    # RESTART
    # -------------------------
    if choice == 0:
        machine.reset()

    # -------------------------
    # POWER OFF
    # -------------------------
    elif choice == 1:
        try:
            M5.Power.powerOff()
        except:
            try:
                Power.powerOff()
            except:
                pass

    # -------------------------
    # DOWNLOAD MODE
    # -------------------------
    elif choice == 2:
        try:
            machine.bootloader()
        except:
            pass

    # -------------------------
    # RETURN
    # -------------------------
    else:
        return
power_menu()
