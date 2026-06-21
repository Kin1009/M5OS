import os
import system

                from text_editor_embed import text_editor  # or 
                    whatever file your text_editor is in

import graphics as g

import ui


# -------------------------
# Helpers
# -------------------------


def is_dir(path):
    try:
        os.listdir(path)
        return True
    except:
        return False



def parent_dir(path):

    if path in ('/', '/flash'):
        return path

    parts = path.rstrip('/').split('/')

    if len(parts) <= 1:
        return '/'

    return '/'.join(parts[:-1]) or '/'



def join_path(a, b):
    if a.endswith('/'):
        return a + b
    return a + '/' + b


# -------------------------
# File menu
# -------------------------


def file_menu(path):

    while True:

        options = ['Edit']

        if path.endswith('.bmp') or path.endswith('.png') or path.endswith('.jpeg'):
            options.append('Display')

        if path.endswith('.py'):
            options.append('Execute')

        options.extend([
            'Rename',
            'Copy',
            'Move',
            'Delete',
            'Back'
        ])

        choice = ui.chooser(options, label=path)
        action = options[choice]

        # -------------------------
        # Back
        # -------------------------

        if action == "Back":
            return

        # -------------------------
        # Edit (placeholder)
        # -------------------------

        elif action == "Edit":

            try:

                text_editor(path)

            except Exception as e:
                ui.chooser([str(e)], label='Error')

        # -------------------------
        # Display image
        # -------------------------

        elif action == "Display":

            while True:

                g.canvas.fillScreen(0)

                try:
                    g.canvas.drawImage(path, 0, 0)
                    g.canvas.push(0, 0)

                except Exception as e:
                    ui.chooser([str(e)], label="Image Error")
                    break

                if system.key1_just_pressed() or system.key2_just_pressed():
                    break

        # -------------------------
        # Execute
        # -------------------------

        elif action == "Execute":
            system.safe_run_app(path)

        # -------------------------
        # Rename
        # -------------------------

        elif action == "Rename":

            new_name = ui.input("New name:")

            if not new_name:
                continue

            try:
                parent = path.rsplit('/', 1)[0]
                new_path = join_path(parent, new_name)
                os.rename(path, new_path)
                return

            except Exception as e:
                ui.chooser([str(e)], label="Rename Error")

        # -------------------------
        # Copy
        # -------------------------

        elif action == "Copy":

            try:
                dest_dir = ui.dirchooser('/flash')
                if not dest_dir:
                    continue

                name = path.split('/')[-1]
                dest = join_path(dest_dir, name)

                with open(path, 'rb') as f:
                    data = f.read()

                with open(dest, 'wb') as f:
                    f.write(data)

                ui.chooser(["Copy done"], label='Success')

            except Exception as e:
                ui.chooser([str(e)], label="Copy Error")

        # -------------------------
        # Move
        # -------------------------

        elif action == "Move":

            try:
                dest_dir = ui.dirchooser('/flash')
                if not dest_dir:
                    continue

                name = path.split('/')[-1]
                dest = join_path(dest_dir, name)

                os.rename(path, dest)

                ui.chooser(["Move done"], label='Success')
                return

            except Exception as e:
                ui.chooser([str(e)], label="Move Error")

        # -------------------------
        # Delete
        # -------------------------

        elif action == "Delete":

            confirm = ui.chooser(['No', 'Yes'], label='Delete?')

            if confirm == 1:
                try:
                    os.remove(path)
                    ui.chooser(['Deleted'], label='OK')
                    return
                except Exception as e:
                    ui.chooser([str(e)], label="Delete Error")


# -------------------------
# Explorer
# -------------------------


def explorer(start='/flash'):

    cwd = start

    while True:

        entries = []

        # root handling
        if cwd == "/flash":
            entries.append('Exit')
        else:
            entries.append('..')

        # directory listing
        try:
            names = sorted(os.listdir(cwd))
        except:
            names = []

        for name in names:

            full = join_path(cwd, name)

            if is_dir(full):
                entries.append("[D] " + name)
            else:
                entries.append(name)

        # NEW actions belong to folder, not file
        entries.append("[New File]")
        entries.append("[New Folder]")

        choice = ui.chooser(entries, label=cwd)
        selected = entries[choice]

        # -------------------------
        # Exit
        # -------------------------

        if selected == "Exit":
            return

        # -------------------------
        # Parent
        # -------------------------

        if selected == "..":
            cwd = parent_dir(cwd)
            continue

        # -------------------------
        # New File
        # -------------------------

        if selected == "[New File]":

            name = ui.input("File name:")

            if name:
                try:
                    with open(join_path(cwd, name), 'w') as f:
                        f.write('')
                except:
                    pass

            continue

        # -------------------------
        # New Folder
        # -------------------------

        if selected == "[New Folder]":

            name = ui.input("Folder name:")

            if name:
                try:
                    os.mkdir(join_path(cwd, name))
                except:
                    pass

            continue

        # -------------------------
        # Open folder
        # -------------------------

        if selected.startswith("[D] "):

            cwd = join_path(cwd, selected[4:])
            continue

        # -------------------------
        # Open file
        # -------------------------

        file_menu(join_path(cwd, selected))


explorer('/flash')
