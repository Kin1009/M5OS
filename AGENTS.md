# M5OS Project Guidance

M5OS is a lightweight operating system and application framework written in MicroPython for the M5Stack StickS3. It is not trying to emulate Linux, Android, or a desktop OS. Prefer simple, maintainable, resource-aware code that starts fast and gives apps consistent shared APIs.

## Target Hardware

- Primary target: M5Stack StickS3.
- Expected features: ESP32, 240x135 LCD, battery, WiFi, Bluetooth, speaker, K1/K2 buttons, RTC/time sync, and optional IMU.
- Avoid desktop assumptions and heavy dependencies.

## Project Philosophy

- Simple over complex.
- Pure Python when practical.
- Fast startup.
- Minimal dependencies.
- Consistent app behavior and safe launching.
- Human-readable JSON configuration.
- Maintainability and developer ergonomics over feature count.

## Filesystem Layout

- Apps live under `/flash/apps/`, usually one folder per app.
- Config files live under `/flash/config/`.
- Common config files include `/flash/config/settings.json` and `/flash/config/wifi.json`.
- System fonts live under `/system/common/font/`.
- Preferred fonts include:
  - `/system/common/font/Montserrat-Medium-10.vlw`
  - `/system/common/font/Montserrat-Medium-12.vlw`
  - `/system/common/font/Montserrat-Medium-14.vlw`
  - `/system/common/font/Montserrat-Medium-18.vlw`

## Graphics And UI

- Apps typically use `import graphics as g`, call `g.init()`, draw on `g.canvas`, then call `canvas.push(0, 0)`.
- Common canvas methods include `fillScreen`, `fillRect`, `fillCircle`, `setCursor`, `setTextColor`, `print`, and `drawImage`.
- The UI framework should stay lightweight. Apps usually draw directly to the canvas rather than using a complex retained-mode GUI.
- Preferred visual style: dark theme, clean layouts, minimal clutter, consistent spacing, white text, dark grey panels, and muted accent colors.
- Avoid flashing colors, excessive debug information, overcrowded layouts, and placeholder-looking UI.

## Navigation

- K1 should generally open the Apps Menu.
- K2 should generally open the Power Menu.
- Home-screen style apps should preserve this behavior.
- Launch apps with `system.safe_run_app(path)`, for example:
  - `/flash/apps/apps/apps.py`
  - `/flash/apps/power/power.py`

## Startup Screen

Startup is the primary home screen. It should:

- Show wallpaper or an efficient animation.
- Show a top status bar.
- Show time, battery, and WiFi status.
- Handle K1 and K2 navigation.
- Start or update WiFi services.

Keep wallpaper animations efficient and responsive. Previously explored styles include matrix effects, particles, waves, collision simulations, radar sweeps, flow fields, and hexadecimal displays.

## Top Bar

- Typical height: `TOPBAR_H = 16`.
- Left side usually shows WiFi status and time.
- Right side usually shows battery percentage and charging status.
- Draw the top bar after the background so it remains visible.

## System API

Apps commonly import `system`.

Expected helpers include:

- WiFi: `wifi_connect`, `wifi_update`, `wifi_status`, `wifi_label`.
- Time: `time_label`.
- Battery: `battery_level`.
- Buttons: `key1_just_pressed`, `key2_just_pressed`.
- Launching: `safe_run_app`.

## WiFi Manager

The WiFi manager should:

- Auto-connect on boot when enabled.
- Load saved networks from `/flash/config/wifi.json`.
- Scan available networks.
- Prefer the strongest saved network.
- Fall back to open networks when appropriate.
- Expose connection state.

Common states are `CONNECTED`, `CONNECTING`, `FAIL`, and `ERROR`.

## Settings

- Store settings in `/flash/config/settings.json`.
- Use human-readable JSON.
- Example: `{"autowifi": true}`.

## Built-In Apps

- Weather should auto-detect location, display current weather with modern styling, use Montserrat fonts, refresh on demand, and avoid debug-style layouts.
- Calendar targets a simple weekly view with event groups, colors, repeating events, day-based schedules, and time-based schedules.
- Audio-capable future apps may include Bluetooth speaker, notification sounds, media playback, and alarm clock features.

## Performance

- Minimize allocations.
- Reuse objects where possible.
- Avoid excessive file I/O.
- Avoid unnecessary redraws.
- Prefer simple algorithms.
- Keep animations responsive while still allowing button input and WiFi updates.
