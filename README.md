# Steam Controller 2 Bridge for Batocera

Experimental userspace Bluetooth support for the **Steam Controller 2** on Batocera.

## Current Status

Working on **Steam Deck**.

Batocera detects the Steam Controller 2 over Bluetooth as Valve device:

```text
28DE:1303
```

but the current `hid-steam` driver does not bind to that product ID.

Linux still exposes the controller's raw Bluetooth HID reports, so this project reads those reports directly and converts them into a normal virtual Linux gamepad using `uinput` and `python-evdev`.

**No kernel modification is required.**

## How It Works

```text
Steam Controller 2
        |
        | Bluetooth
        v
raw HID device
        |
        v
sc2bridge.py
        |
        | uinput / evdev
        v
virtual Linux gamepad
        |
        v
Batocera / EmulationStation / emulators
```

The bridge also temporarily grabs the controller's native Bluetooth keyboard and mouse fallback interfaces while running. This prevents those inputs from interfering with Batocera controller mapping.

## Currently Working

- A / B / X / Y
- D-pad
- LB / RB
- L3 / R3
- View
- Menu
- Steam button
- Left analog stick
- Right analog stick
- Left analog trigger
- Right analog trigger
- Stick dead zones
- Automatic detection of the Steam Controller 2 HID device

The controller can currently be configured and used as a standard gamepad in Batocera.

## Not Yet Implemented

- Rear buttons
- QAM button
- Trackpads
- Gyroscope
- Rumble / haptics
- Automatic installation
- Automatic startup

These are planned for later development.

## Requirements

- Batocera
- Steam Controller 2 paired over Bluetooth
- Python 3
- `python-evdev`
- Linux `uinput`

## Files

```text
sc2bridge.py
start-sc2bridge.sh
stop-sc2bridge.sh
README.md
LICENSE
```

## Installation

Copy these files to:

```text
/userdata/system/sc2bridge.py
/userdata/system/start-sc2bridge.sh
/userdata/system/stop-sc2bridge.sh
```

Make them executable:

```bash
chmod +x /userdata/system/sc2bridge.py
chmod +x /userdata/system/start-sc2bridge.sh
chmod +x /userdata/system/stop-sc2bridge.sh
```

## Start

```bash
/userdata/system/start-sc2bridge.sh
```

The bridge runs in the background and logs to:

```text
/userdata/system/logs/sc2bridge.log
```

An SSH session does **not** need to remain open while the bridge is running.

## Stop

```bash
/userdata/system/stop-sc2bridge.sh
```

## Controller Mapping

After starting the bridge, open Batocera controller configuration and map:

- A / B / X / Y
- D-pad
- LB / RB
- L3 / R3
- View / Menu / Steam
- Left and right sticks
- Left and right triggers

The D-pad is exposed as digital gamepad buttons rather than hat axes.

## Uninstall

Stop the bridge first:

```bash
/userdata/system/stop-sc2bridge.sh
```

Then remove:

```text
/userdata/system/sc2bridge.py
/userdata/system/start-sc2bridge.sh
/userdata/system/stop-sc2bridge.sh
```

## Known Limitations

This is an experimental work-in-progress.

The current version focuses on standard gamepad functionality only. Additional Steam Controller 2 features such as rear buttons, QAM, trackpads, gyro, and haptics are not implemented yet.

## Project Goal

The first-stage goal was to prove that the Steam Controller 2 could operate as a normal Bluetooth gamepad in Batocera without modifying or rebuilding the kernel.

**That goal has been achieved.**

## License

MIT License. See `LICENSE`.
