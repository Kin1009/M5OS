# M5OS

M5OS is a lightweight operating system and application framework written in MicroPython for the M5Stack StickS3.

It is designed to provide a simple app launcher, shared system services, a graphics layer, WiFi management, configuration storage, and reusable APIs for small applications running on resource-constrained ESP32 hardware.

M5OS is not trying to be Linux, Android, or a desktop-style operating system. The goal is a fast, clean, consistent environment for building useful StickS3 apps in Python.

## Design Goals

- Simple over complex
- Fast startup
- Pure Python when possible
- Minimal dependencies
- Easy app development
- Consistent user experience
- Safe app launching
- JSON-based settings and configuration
- Good performance on small embedded hardware

## Target Hardware

Primary target:

- M5Stack StickS3

Expected hardware features:

- ESP32
- 240x135 LCD
- Battery
- WiFi
- Bluetooth
- Speaker
- K1 and K2 buttons
- RTC/time synchronization
- Optional IMU/accelerometer

The codebase should avoid assumptions that only make sense on desktop systems.

## Filesystem Layout

Applications live under:

```text
/flash/apps/
```

Example app folders:

```text
/flash/apps/startup/
/flash/apps/apps/
/flash/apps/power/
/flash/apps/weather/
/flash/apps/calendar/
```

Configuration files live under:

```text
/flash/config/
```

Common config files:

```text
/flash/config/settings.json
/flash/config/wifi.json
```

System fonts live under:

```text
/system/common/font/
```

Common fonts:

```text
/system/common/font/Montserrat-Medium-10.vlw
/system/common/font/Montserrat-Medium-12.vlw
/system/common/font/Montserrat-Medium-14.vlw
/system/common/font/Montserrat-Medium-18.vlw
```

Apps should use the shared fonts when possible so the interface stays consistent.

## App Model

Each app usually has its own folder inside `/flash/apps/`.

Apps are launched through the shared system API:

```python
import system

system.safe_run_app("/flash/apps/apps/apps.py")
```

The launcher is expected to avoid crashing the whole OS when an app fails.

## Navigation

M5OS uses the two hardware buttons as the primary navigation controls.

Standard behavior:

```text
K1 -> Apps Menu
K2 -> Power Menu
```

Home-screen style apps should preserve this behavior.

## Graphics

M5OS uses a custom graphics abstraction.

Typical app setup:

```python
import graphics as g

g.init()
canvas = g.canvas
```

Common canvas methods include:

```python
canvas.fillScreen(color)
canvas.fillRect(x, y, w, h, color)
canvas.fillCircle(x, y, r, color)

canvas.setCursor(x, y)
canvas.setTextColor(fg)
canvas.setTextColor(fg, bg)
canvas.print(text)

canvas.drawImage(path, x, y)
canvas.push(0, 0)
```

Apps usually draw to the canvas and then call:

```python
canvas.push(0, 0)
```

to update the display.

## System API

Apps commonly import:

```python
import system
```

Useful system helpers include:

```python
system.wifi_connect(ssid, password)
system.wifi_update()
system.wifi_status()
system.wifi_label()

system.time_label()
system.battery_level()

system.key1_just_pressed()
system.key2_just_pressed()

system.safe_run_app(path)
```

These APIs are meant to keep app code simple and consistent.

## Startup Screen

The startup app acts as the home screen.

Its responsibilities include:

- Showing wallpaper or a lightweight animation
- Drawing the top status bar
- Showing time
- Showing battery state
- Showing WiFi state
- Handling K1 and K2 navigation
- Starting or updating WiFi services

Animations should stay responsive and avoid heavy CPU usage.

## Top Bar

Most apps may use a shared top bar style.

Typical contents:

- Left side: WiFi status and time
- Right side: battery percentage and charging status

Typical height:

```python
TOPBAR_H = 16
```

The top bar should be drawn after the background so it remains visible.

## WiFi

M5OS includes a WiFi manager for handling saved networks and connection state.

The WiFi manager should:

- Auto-connect on boot when enabled
- Load saved networks
- Scan available networks
- Prefer the strongest saved known network
- Fall back to open networks when appropriate
- Expose connection state to apps

Saved WiFi networks are stored at:

```text
/flash/config/wifi.json
```

Example:

```json
{
  "HomeWiFi": "password",
  "PhoneHotspot": "secret"
}
```

Common connection states:

```text
CONNECTED
CONNECTING
FAIL
ERROR
```

## Settings

Settings are stored as human-readable JSON files.

Main settings path:

```text
/flash/config/settings.json
```

Example:

```json
{
  "autowifi": true
}
```

## Built-In Apps

M5OS includes or plans to include several built-in apps.

Examples:

- Startup/home screen
- Apps launcher
- Power menu
- Weather
- Calendar
- Settings

The weather app should focus on a clean modern layout, automatic location detection, current conditions, refresh support, and Montserrat fonts.

The calendar app currently targets a simple weekly view with event groups, colors, repeating events, day-based schedules, and time-based schedules.

## Visual Style

Preferred style:

- Dark theme
- Clean layouts
- Minimal clutter
- Consistent spacing
- Smooth but efficient animations
- Black backgrounds
- Dark grey panels
- White text
- Muted accent colors

Avoid:

- Flashing colors
- Excessive debug information
- Overcrowded screens
- Ugly placeholder layouts

## Performance Notes

M5OS runs on constrained embedded hardware, so code should be careful with resources.

Prefer:

- Small modules
- Simple algorithms
- Reused objects
- Minimal allocations
- Limited file I/O
- Focused redraws instead of unnecessary full-screen work

Animations should continue checking buttons and updating WiFi state so the device feels responsive.

## Development Tools

This repository includes helper scripts for packaging and assets.

- `pack.py` helps package firmware files.
- `png_to_bmp.py` helps create UI icons and app icons.

## Repository

GitHub:

```text
https://github.com/Kin1009/M5OS
```

## Contact

- Email: khoi.nguyenminh100912@gmail.com
- Discord: `flys_acc`
- Discord server: https://discord.gg/aWCbmsbcS5
