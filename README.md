# Steam Controller 2 for Batocera

## v1.0.0 — First Stable Release

A userspace Bluetooth bridge that makes the **Steam Controller 2** function as a standard gamepad and mouse in **Batocera** without rebuilding or patching the kernel.

The controller currently appears over Bluetooth as raw HID device `28DE:1303` handled by `hid-generic`. This bridge reads those raw HID reports directly and converts them into standard Linux virtual input devices using **python-evdev** and **uinput**.

---

## What v1.0.0 provides

### Virtual gamepad

The bridge creates:

```text
Steam Controller 2 Bridge
```

Supported controls:

- A / B / X / Y
- D-pad
- Left and right analog sticks
- Analog triggers
- L3 / R3
- LB / RB
- View / Menu / Steam
- QAM
- L4 / L5
- R4 / R5
- Linux `FF_RUMBLE`

Extra buttons are exposed as:

```text
QAM -> BTN_TRIGGER_HAPPY1
L4  -> BTN_TRIGGER_HAPPY2
L5  -> BTN_TRIGGER_HAPPY3
R4  -> BTN_TRIGGER_HAPPY4
R5  -> BTN_TRIGGER_HAPPY5
```

### Virtual mouse

v1.0.0 also creates:

```text
Steam Controller 2 Mouse
```

Trackpad layout:

```text
Right trackpad
  movement -> mouse pointer

Left trackpad
  physical click on left half  -> left mouse button
  physical click on right half -> right mouse button
```

The right trackpad uses relative mouse output with filtering and smoothing to reduce raw HID coordinate jitter.

---

## Force feedback / rumble

The virtual gamepad exposes Linux:

```text
FF_RUMBLE
```

The bridge receives force-feedback effects from games and emulators and translates them into Steam Controller 2 Bluetooth HID output report `0x80`.

Confirmed behavior includes:

- force-feedback effect upload
- play
- stop
- erase
- independent left/right haptic channels
- real in-game rumble through Batocera/Wine
- rumble recovery after controller reconnect

Current practical haptic settings:

```text
HAPTIC_SPEED = 18000
HAPTIC_MAX_GAIN = 128
```

A zero-magnitude request sends a true stop packet so the controller does not retain a light baseline vibration.

---

## Bluetooth identity

Confirmed Bluetooth HID identity:

```text
Bus:     0005
Vendor:  28DE
Product: 1303
HID_ID:  0005:000028DE:00001303
Driver:  hid-generic
```

The bridge discovers the raw HID device dynamically and does **not** rely on a fixed `/dev/hidrawX` number.

This Bluetooth HID identity has been independently confirmed on **two separate Steam Controller 2 units**.

---

## Automatic reconnect

The included watcher and Batocera service handle controller lifecycle automatically.

When the controller is powered off:

- the bridge exits
- the virtual controller disappears
- the virtual mouse disappears
- no ghost controller is left behind

When the controller powers back on:

- BlueZ reconnect is requested
- the watcher waits for raw HID to appear
- the bridge restarts
- the gamepad and mouse are recreated
- force feedback becomes available again

After repeated reconnect failures, the watcher can power-cycle the Bluetooth adapter and retry.

> **Note:** resetting the Bluetooth adapter can briefly disconnect other Bluetooth devices.

---

## Installation

The v1.0.0 release includes a self-contained installer:

```text
sc2-installer-v1.0.0.sh
```

Copy it to your Batocera system and run:

```bash
bash sc2-installer-v1.0.0.sh
```

The installer:

- checks required dependencies
- preserves existing managed files for rollback
- installs the bridge
- installs the reconnect watcher
- installs the Batocera service
- installs project documentation
- enables and starts the service

Useful installer commands:

```bash
bash sc2-installer-v1.0.0.sh check
bash sc2-installer-v1.0.0.sh status
bash sc2-installer-v1.0.0.sh uninstall
```

Enable automatic startup from Batocera:

```text
MAIN MENU
-> SYSTEM SETTINGS
-> SERVICES
-> SteamController2
```

Or manage it over SSH:

```bash
batocera-services start SteamController2
batocera-services stop SteamController2
batocera-services restart SteamController2
```

---

## Installed files

```text
/userdata/system/sc2bridge.py
/userdata/system/sc2watcher.sh
/userdata/system/services/SteamController2
```

Log:

```text
/userdata/system/logs/sc2bridge.log
```

View recent log output:

```bash
tail -n 100 /userdata/system/logs/sc2bridge.log
```

---

## Verify the virtual devices

After the controller is connected:

```bash
grep -A12 -E 'Name="Steam Controller 2 (Bridge|Mouse)"' /proc/bus/input/devices
```

Expected devices:

```text
Steam Controller 2 Bridge
Steam Controller 2 Mouse
```

The gamepad should expose force feedback:

```text
B: FF=10000 0
```

The mouse should expose relative movement:

```text
REL_X
REL_Y
BTN_LEFT
BTN_RIGHT
```

---

## Validation

The following have been confirmed during development:

- standard gamepad controls
- analog sticks and triggers
- QAM / L4 / L5 / R4 / R5
- Bluetooth disconnect/reconnect lifecycle
- automatic bridge recreation
- Linux `FF_RUMBLE`
- independent left/right haptic output
- real in-game rumble through Batocera/Wine
- right-trackpad mouse movement
- left-pad left/right mouse clicks
- dynamic raw HID discovery
- fallback Bluetooth keyboard/mouse interface grabbing

Core controller operation was independently validated on a second Steam Controller 2 unit.

---

## Known limitations

- Right-trackpad mouse movement is usable, but future releases may continue refining pointer feel and smoothing.
- Gyro is not currently implemented.
- Capacitive stick/grip/side-touch inputs are not exposed as separate user-facing controls.
- This is a userspace compatibility bridge, not a replacement Linux kernel driver.
- Development and validation have focused on Batocera v43.

---

## Project history

The bridge grew through several working milestones:

```text
v0.1.0  Manual userspace bridge
v0.2.0  Batocera service + automatic reconnect
v0.2.1  Bluetooth recovery handling
v0.3.0  QAM / L4 / L5 / R4 / R5
v0.4.0  Trackpad analog support
v0.5.0  Force feedback / rumble
v0.8.0  Controller + mouse redesign
v1.0.0  First stable packaged release
```

---

## Credits

Developed and tested through **Vesra's Workshop**.

Independent controller testing helped confirm the Bluetooth identity and core controller behavior on a second Steam Controller 2 unit.

---

## License

MIT License. See `LICENSE`.

---

**If it runs, ship it. If it doesn't, it WILL be SSH'ed.**
