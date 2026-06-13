import machine
import ui

def power_menu():

    choice = ui.chooser(
        [
            "Restart",
            "Power off",
            "Download mode",
            "Return"
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
            import M5
            M5.Power.powerOff()
        except:
            try:
                import Power
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