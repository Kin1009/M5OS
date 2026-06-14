import ui
import system
import gc


def safe_exec(code, env):

    try:
        exec(code, env, env)
    except Exception as e:
        return str(e)

    return None


def repl():

    env = {
        "__name__": "__main__",
        "system": system,
        "ui": ui,
    }

    buffer = ""

    while True:

        menu = [
            "Run Code",
            "Edit Code",
            "Clear",
            "Exit"
        ]

        choice = ui.chooser(menu, label="Python REPL")

        action = menu[choice]

        # -------------------------
        # EXIT
        # -------------------------
        if action == "Exit":
            return

        # -------------------------
        # CLEAR
        # -------------------------
        if action == "Clear":
            buffer = ""
            continue

        # -------------------------
        # EDIT CODE
        # -------------------------
        if action == "Edit Code":

            new_code = ui.input("Enter Python code")

            if new_code is not None:
                buffer = new_code

            continue

        # -------------------------
        # RUN CODE
        # -------------------------
        if action == "Run Code":

            gc.collect()

            if not buffer:
                ui.chooser(["No code"], label="REPL")
                continue

            err = safe_exec(buffer, env)

            if err:
                ui.chooser(err.split("\n"), label="Error")
            else:
                ui.chooser(["OK"], label="Output")


repl()