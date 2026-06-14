import os
import json
import sys
import base64


def format_size(size):

    units = ["B", "KB", "MB", "GB"]

    value = float(size)
    unit = 0

    while value >= 1024 and unit < len(units) - 1:
        value /= 1024
        unit += 1

    return f"{value:.2f} {units[unit]}"


def pack(root, version, numeric_version):

    root = os.path.abspath(root)
    root_name = os.path.basename(root)

    bundle = {
        "__version__": version,
        "__numeric_version__": numeric_version,
        "files": {}
    }

    file_count = 0

    for current, dirs, files in os.walk(root):

        # Exclude /flash/config
        if "config" in dirs:
            dirs.remove("config")

        for filename in files:

            full = os.path.join(current, filename)

            rel = os.path.relpath(full, root)

            flash_path = "/" + root_name + "/" + rel.replace("\\", "/")

            try:

                with open(
                    full,
                    "r",
                    encoding="utf-8"
                ) as f:

                    bundle["files"][flash_path] = {
                        "type": "text",
                        "data": f.read()
                    }

            except UnicodeDecodeError:

                with open(full, "rb") as f:

                    bundle["files"][flash_path] = {
                        "type": "binary",
                        "data": base64.b64encode(
                            f.read()
                        ).decode("ascii")
                    }

            file_count += 1

    out_name = root_name + ".json"

    with open(
        out_name,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            bundle,
            f,
            indent=4,
            ensure_ascii=False
        )

    size = os.path.getsize(out_name)

    print("Output :", out_name)
    print("Version:", version)
    print("Build  :", numeric_version)
    print("Files  :", file_count)
    print("Size   :", format_size(size))
    print("Bytes  :", size)


if __name__ == "__main__":

    if len(sys.argv) != 4:

        print(
            "Usage: pack <root> <version> <numeric_version>"
        )

        sys.exit(1)

    pack(
        sys.argv[1],
        sys.argv[2],
        int(sys.argv[3])
    )