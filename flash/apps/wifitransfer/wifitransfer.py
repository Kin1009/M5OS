import network
import socket
import time
import os
import system
import graphics as g
import random
UPLOAD_DIR = "/flash/uploads"


# -------------------------
# LOGGING
# -------------------------
def log(lines):
    c = g.canvas
    c.fillScreen(0x000000)
    c.setTextColor(0xFFFFFF)

    y = 5
    for line in lines[-12:]:
        c.setCursor(5, y)
        c.print(str(line))
        y += 14

    c.push(0, 0)


# -------------------------
# FILE SYSTEM
# -------------------------
def ensure_dir():
    try:
        os.listdir(UPLOAD_DIR)
    except:
        try:
            os.mkdir(UPLOAD_DIR)
        except:
            pass


def save_file(name, data):
    ensure_dir()

    safe = name.replace("/", "_")
    path = UPLOAD_DIR + "/" + safe

    try:
        with open(path, "wb") as f:
            f.write(data)
        return path
    except:
        return None


# -------------------------
# HTML + JS (NO MULTIPART)
# -------------------------
HTML = """\
HTTP/1.1 200 OK

<html>
<head>
<style>
body {
    background:#111;
    color:white;
    font-family:Arial;
    text-align:center;
}

.box {
    margin-top:50px;
    padding:20px;
    background:#222;
    display:inline-block;
    border-radius:10px;
}

input, button {
    margin:10px;
    padding:8px;
}

button {
    background:#00aa00;
    border:none;
    color:white;
}
</style>
</head>

<body>

<div class="box">
<h2>StickS3 Transfer</h2>

<input type="text" id="fname" placeholder="filename"><br>
<input type="file" id="file"><br>

<button onclick="send()">Upload</button>

<p id="status"></p>
</div>

<script>
function send() {
    let f = document.getElementById("file").files[0];
    let name = document.getElementById("fname").value;

    if (!f) {
        document.getElementById("status").innerText = "No file";
        return;
    }

    let reader = new FileReader();

    reader.onload = function() {
        fetch("/", {
            method: "POST",
            headers: {
                "X-Filename": name || f.name
            },
            body: reader.result
        }).then(() => {
            document.getElementById("status").innerText = "Uploaded";
        });
    };

    reader.readAsArrayBuffer(f);
}
</script>

</body>
</html>
"""


# -------------------------
# SERVER
# -------------------------
def start_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(2)
    
    return s


# -------------------------
# MAIN
# -------------------------
def main():

    logs = []

    ap = network.WLAN(network.AP_IF)
    ap.active(True)

    ssid = "StickS3"
    password = "".join(str(random.randint(0, 9)) for i in range(8))

    try:
        ap.config(
            essid=ssid,
            password=password,
            authmode=network.AUTH_WPA_WPA2_PSK
        )
    except:
        ap.config(essid=ssid, password=password)

    logs.append("AP: StickS3")
    logs.append("PASS: " + password)
    logs.append("IP: 192.168.4.1")
    log(logs)

    server = start_server()
    server.settimeout(0.2)
    logs.append("Server ready")
    log(logs)

    system._wifi_state = "AP"

    # -------------------------
    # LOOP
    # -------------------------
    while True:
        print("tick")
        # EXIT
        if system.key1_pressed() or system.key2_pressed():
            logs.append("EXIT")
            log(logs)
            return

        try:
            cl, addr = server.accept()
            req = cl.recv(8192)

            if not req:
                cl.close()
                continue

            logs.append("Client: " + str(addr))

            # -------------------------
            # RAW UPLOAD (NO PARSING)
            # -------------------------
            if "POST" in str(req):

                try:
                    headers, body = req.split(b"\r\n\r\n", 1)

                    filename = "upload.bin"

                    try:
                        hstr = str(headers)
                        if "X-Filename:" in hstr:
                            filename = hstr.split("X-Filename:")[1].split("\\r\\n")[0].strip()
                    except:
                        pass

                    path = save_file(filename, body)

                    logs.append("Saved:")
                    logs.append(str(path))

                except Exception as e:
                    logs.append("UPLOAD FAIL")
                    logs.append(str(e))

                log(logs)

            # ALWAYS RESPOND
            cl.send(HTML)
            cl.close()

        except Exception as e:
            if not ("116" in str(e)):
                logs.append("ERR")
                logs.append(str(e))
                log(logs)


main()