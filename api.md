# M5OS Library Reference

## `flash/libs/graphics.py`

| Function                                                                 | Purpose                                                                          |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| `init()`                                                                 | Initializes M5 display state, rotation, canvas, and default font.                |
| `update_system(new_list)`                                                | Replaces the system-layer drawable object list.                                  |
| `update(new_list)`                                                       | Replaces the user-layer drawable object list.                                    |
| `flatten(scene)`                                                         | Flattens nested drawable lists into a single list.                               |
| `render(bg=0x000000)`                                                    | Clears the canvas, draws system objects, draws user objects, then pushes to LCD. |
| `UIObject.draw(self, canvas)`                                            | Base drawable stub for UI objects.                                               |
| `Text.__init__(self, text, fg, x, y, bg=None)`                           | Stores text drawing parameters.                                                  |
| `Text.draw(self, c)`                                                     | Draws text at the configured position and colors.                                |
| `Rectangle.__init__(self, color, x, y, w, h)`                            | Stores rectangle drawing parameters.                                             |
| `Rectangle.draw(self, c)`                                                | Draws a filled rectangle.                                                        |
| `Circle.__init__(self, color, x, y, r)`                                  | Stores circle drawing parameters.                                                |
| `Circle.draw(self, c)`                                                   | Draws a filled circle.                                                           |
| `Line.__init__(self, color, x1, y1, x2, y2)`                             | Stores line drawing parameters.                                                  |
| `Line.draw(self, c)`                                                     | Draws a line.                                                                    |
| `BorderedRectangle.__init__(self, x, y, w, h, border_color, fill_color)` | Builds a bordered rectangle from two rectangles.                                 |
| `BorderedRectangle.draw(self, c)`                                        | Draws the filled rectangle and border.                                           |

---

## `flash/libs/system.py`

| Function                       | Purpose                                                                  |
| ------------------------------ | ------------------------------------------------------------------------ |
| `ntp_sync()`                   | Synchronizes RTC time via NTP when WiFi is connected.                    |
| `exception_to_string(exc)`     | Converts an exception traceback into a string.                           |
| `battery_level()`              | Reads battery percentage using available M5 power APIs.                  |
| `key1_pressed()`               | Returns whether K1 is currently pressed.                                 |
| `key2_pressed()`               | Returns whether K2 is currently pressed.                                 |
| `key1_just_pressed()`          | Detects a new K1 press and plays a click tone.                           |
| `key2_just_pressed()`          | Detects a new K2 press and plays a click tone.                           |
| `safe_run_app(path)`           | Loads and executes an app file, showing an exception chooser on failure. |
| `wifi_scan()`                  | Scans nearby WiFi access points and returns SSID/RSSI/auth info.         |
| `wifi_connect(ssid, password)` | Starts a WiFi connection attempt.                                        |
| `wifi_update()`                | Advances WiFi connection state and handles timeout failure.              |
| `wifi_status()`                | Returns current WiFi state.                                              |
| `wifi_label()`                 | Returns compact WiFi label text for UI.                                  |
| `get_timezone_offset()`        | Reads timezone setting and returns hour offset.                          |
| `time_label()`                 | Returns current local time label as HH:MM.                               |

---

## `flash/libs/wifi_manager.py`

| Function          | Purpose                                                                              |
| ----------------- | ------------------------------------------------------------------------------------ |
| `load_wifi()`     | Loads saved WiFi credentials from config.                                            |
| `start()`         | Starts auto-connect by scanning networks and trying saved/open networks by strength. |
| `_next_network()` | Attempts the next saved or open network after failure.                               |
| `update()`        | Polls connection progress and advances to next network when needed.                  |
| `connected()`     | Returns whether WiFi is connected.                                                   |
| `status()`        | Returns current WiFi status string.                                                  |
| `label()`         | Returns compact WiFi label text.                                                     |
| `done()`          | Returns whether the manager has finished trying networks.                            |

---

## `flash/libs/ui.py`

| Function                                                    | Purpose                                                       |
| ----------------------------------------------------------- | ------------------------------------------------------------- |
| `Chooser.__init__(self, items, x, y, fg=0xFFFFFF, bg=None)` | Stores chooser items and drawing options.                     |
| `Chooser.next(self)`                                        | Moves selection forward with wraparound.                      |
| `Chooser.prev(self)`                                        | Moves selection backward with wraparound.                     |
| `Chooser.get(self)`                                         | Returns selected index.                                       |
| `Chooser.draw(self, c)`                                     | Draws a scrolling text chooser.                               |
| `wrap_text(text, width)`                                    | Splits text into fixed-width chunks.                          |
| `index_to_y(index, length)`                                 | Maps list index to vertical scrollbar position.               |
| `check_exit()`                                              | Detects K1+K2 hold for exit.                                  |
| `find_exit_or_return(items)`                                | Finds a likely exit/back item index.                          |
| `chooser(...)`                                              | Interactive list chooser using K1/K2.                         |
| `draw_button(...)`                                          | Draws a keypad button.                                        |
| `keypad(prompt="Enter number")`                             | Numeric keypad input UI.                                      |
| `button_label(key)`                                         | Converts an input key group into a short button label.        |
| `draw_input_button(...)`                                    | Draws a text-input keyboard button.                           |
| `wifi_input(prompt="Enter text:")`                          | Opens a temporary WiFi AP and web form to collect text input. |
| `url_decode(s)`                                             | Decodes URL form text.                                        |
| `input(prompt="Enter text:")`                               | Chooses WiFi or local text input based on settings.           |
| `local_input(prompt="Enter text:")`                         | On-device text entry UI using K1/K2.                          |
| `_is_dir(path)`                                             | Returns whether a path is a directory.                        |
| `_parent_dir(path)`                                         | Returns parent directory path.                                |
| `dirchooser(start="/flash")`                                | Interactive folder chooser.                                   |
| `_parent(path)`                                             | Returns parent path while preserving root.                    |
| `getfile(start="/flash")`                                   | Interactive file picker with file creation support.           |

---

## `flash/libs/text_editor_embed.py`

| Function                 | Purpose                            |
| ------------------------ | ---------------------------------- |
| `text_editor(path=None)` | Simple line-based text editor.     |
| `load(p)`                | Reads a file into a list of lines. |

---

## `flash/libs/ir.py`

| Function                         | Purpose                                                     |
| -------------------------------- | ----------------------------------------------------------- |
| `init()`                         | Initializes and returns the hardware IR object.             |
| `_internal_cb(data, addr, ctrl)` | Stores last received IR data and forwards to user callback. |
| `rx_start(callback=None)`        | Starts IR receive callback handling.                        |
| `rx_get()`                       | Returns last received `(data, addr)` tuple.                 |
| `rx_clear()`                     | Clears stored received IR data.                             |
| `tx(data, addr=0)`               | Sends IR data.                                              |
| `status()`                       | Returns OFF or READY.                                       |

---

## `flash/libs/config_store.py`

| Function                        | Purpose                                    |
| ------------------------------- | ------------------------------------------ |
| `load_json(path, default=None)` | Loads JSON from disk.                      |
| `save_json(path, data)`         | Saves JSON data to disk.                   |
| `load_settings()`               | Loads settings and fills missing defaults. |
| `save_settings(cfg)`            | Saves settings.                            |
| `load_wifi()`                   | Loads WiFi configuration.                  |
| `save_wifi(cfg)`                | Saves WiFi configuration.                  |

---

## `flash/libs/requests`

### Response Methods

| Function                     | Purpose                              |
| ---------------------------- | ------------------------------------ |
| `Response.__init__(self, f)` | Wraps a socket/file response stream. |
| `Response.close(self)`       | Closes response stream.              |
| `Response.content(self)`     | Returns raw response bytes.          |
| `Response.text(self)`        | Returns decoded response text.       |
| `Response.json(self)`        | Parses response JSON.                |

### HTTP Functions

| Function            | Purpose                                    |
| ------------------- | ------------------------------------------ |
| `request(...)`      | Generic HTTP/HTTPS request implementation. |
| `head(url, **kw)`   | Sends HEAD request.                        |
| `get(url, **kw)`    | Sends GET request.                         |
| `post(url, **kw)`   | Sends POST request.                        |
| `put(url, **kw)`    | Sends PUT request.                         |
| `patch(url, **kw)`  | Sends PATCH request.                       |
| `delete(url, **kw)` | Sends DELETE request.                      |

---

## `flash/libs/urequests.py`

| Function            | Purpose                                  |
| ------------------- | ---------------------------------------- |
| `__getattr__(attr)` | Backward-compatible proxy to `requests`. |

---

## `flash/libs/base64.py`

Provides Base64, Base32, and Base16 encoding/decoding support, plus legacy file-based helpers and compatibility functions.

Notable functions:

* `b64encode()`
* `b64decode()`
* `standard_b64encode()`
* `standard_b64decode()`
* `urlsafe_b64encode()`
* `urlsafe_b64decode()`
* `b32encode()`
* `b32decode()`
* `b16encode()`
* `b16decode()`
* `encode()`
* `decode()`
* `encodebytes()`
* `decodebytes()`
* `main()`
* `test()`

---

## `flash/libs/binascii.py`

| Function                        | Purpose                                         |
| ------------------------------- | ----------------------------------------------- |
| `unhexlify(data)`               | Hex decoder fallback implementation.            |
| `_transform(n)`                 | Converts Base64 lookup entries into characters. |
| `a2b_base64(ascii)`             | Decodes Base64 data.                            |
| `b2a_base64(bin, newline=True)` | Encodes bytes as Base64.                        |
