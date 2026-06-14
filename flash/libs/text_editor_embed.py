import ui
import system


def text_editor(path=None):

    # -------------------------
    # Pick file if none given
    # -------------------------

    if not path:
        path = ui.getfile("/flash")
        if not path:
            return

    # -------------------------
    # Load file
    # -------------------------

    def load(p):

        try:
            with open(p, "r") as f:
                data = f.read()
            return data.split("\n")
        except:
            return [""]

    lines = load(path)

    if len(lines) == 0:
        lines = [""]

    # -------------------------
    # Main loop
    # -------------------------

    while True:

        display = lines + ["[Add line]", "[Exit]"]

        choice = ui.chooser(
            display,
            "Edit: " + path,
            13
        )

        # -------------------------
        # Exit → save + quit editor
        # -------------------------

        if choice == len(lines) + 1:

            try:
                with open(path, "w") as f:
                    f.write("\n".join(lines))
            except:
                pass

            return

        # -------------------------
        # Add line
        # -------------------------

        if choice == len(lines):

            new_line = ui.input("New line:")

            if new_line is not None:
                lines.append(new_line)

            continue

        # -------------------------
        # Line actions
        # -------------------------

        idx = choice

        action = ui.chooser(
            [
                "Edit line",
                "Delete line",
                "Insert above",
                "Insert below",
                "Back"
            ],
            label="Line " + str(idx)
        )

        # back
        if action == 4:
            continue

        # -------------------------
        # Edit
        # -------------------------

        if action == 0:

            new_text = ui.input("Edit line")

            if new_text is not None:
                lines[idx] = new_text

        # -------------------------
        # Delete
        # -------------------------

        elif action == 1:

            if len(lines) > 1:
                lines.pop(idx)
            else:
                lines[0] = ""

        # -------------------------
        # Insert above
        # -------------------------

        elif action == 2:

            new_text = ui.input("Insert above")

            if new_text is not None:
                lines.insert(idx, new_text)

        # -------------------------
        # Insert below
        # -------------------------

        elif action == 3:

            new_text = ui.input("Insert below")

            if new_text is not None:
                lines.insert(idx + 1, new_text)


