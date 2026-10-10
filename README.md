# Steam Controller 2 for Batocera — v0.8.0 Repo Update

## v0.8.0 — Controller + Mouse Refinement

This update keeps the existing Steam Controller 2 Bluetooth userspace bridge intact while giving the trackpads a more practical desktop-style role.

The virtual controller has also been renamed from `Vesra Steam Controller 2 Bridge` to the neutral:

```text
Steam Controller 2 Bridge
```

A second virtual input device is now created for mouse functionality:

```text
Steam Controller 2 Mouse
```

## What changed

### Right trackpad → mouse movement

The right trackpad now drives a separate relative mouse device using:

```text
REL_X
REL_Y
```

Raw trackpad movement is converted from the Steam Controller 2 absolute pad coordinates into relative mouse movement.

A small noise filter and smoothing layer were added after testing showed that direct frame-to-frame coordinate conversion produced visible cursor jitter.

Current tuning:

```text
MOUSE_DIVISOR = 120
MOUSE_MAX_STEP = 60
MOUSE_NOISE = 220
MOUSE_SMOOTHING = 0.65
```

The result is substantially smoother and usable for pointer control while still remaining responsive.

### Left trackpad → mouse buttons

The left trackpad now supplies mouse button control while retaining the pad's physical-click requirement.

```text
Click left half  -> left mouse button
Click right half -> right mouse button
```

Simply touching the pad does not click. The physical pad click must be pressed, which reduces accidental mouse input.

### Trackpad analog axes removed from the gamepad

Previous releases exposed the pads as:

```text
ABS_HAT1X / ABS_HAT1Y
ABS_HAT2X / ABS_HAT2Y
```

Those extra analog axes have been removed from the virtual gamepad in v0.8.0.

The pads now serve the dedicated mouse functions instead.

## Existing functionality retained

- Standard face buttons
- D-pad
- Analog sticks
- Analog triggers
- L3 / R3
- LB / RB
- View / Menu / Steam
- QAM
- L4 / L5
- R4 / R5
- Linux `FF_RUMBLE`
- Independent left/right controller haptics
- Bluetooth reconnect watcher
- Bluetooth recovery after repeated reconnect failures
- Fallback Steam Controller Bluetooth keyboard/mouse interface grabbing
- Automatic raw HID discovery by `28DE:1303`

## Virtual devices

v0.8.0 creates two virtual devices:

```text
Steam Controller 2 Bridge
Steam Controller 2 Mouse
```

The gamepad continues to advertise force feedback.

Example gamepad capability:

```text
B: FF=10000 0
```

The mouse device exposes:

```text
REL_X
REL_Y
BTN_LEFT
BTN_RIGHT
```

## Force Feedback

Force feedback remains based on Steam Controller 2 Bluetooth HID output report `0x80`.

Current practical haptic settings remain:

```text
HAPTIC_SPEED = 18000
HAPTIC_MAX_GAIN = 128
```

Linux rumble magnitude `0` sends a true stop packet.

## Extra Button Mapping

```text
QAM -> BTN_TRIGGER_HAPPY1
L4  -> BTN_TRIGGER_HAPPY2
L5  -> BTN_TRIGGER_HAPPY3
R4  -> BTN_TRIGGER_HAPPY4
R5  -> BTN_TRIGGER_HAPPY5
```

## Bluetooth HID Identity

Confirmed Steam Controller 2 Bluetooth identity:

```text
Bus:     0005
Vendor:  28DE
Product: 1303
HID_ID:  0005:000028DE:00001303
Driver:  hid-generic
```

This identity has been independently confirmed on two separate Steam Controller 2 units.

The bridge does not depend on a fixed `/dev/hidrawX` device number.

## Install paths

```text
/userdata/system/sc2bridge.py
/userdata/system/sc2watcher.sh
/userdata/system/services/SteamController2
```

Enable the service from Batocera:

```text
MAIN MENU
> SYSTEM SETTINGS
> SERVICES
> SteamController2
```

Or start it over SSH:

```bash
batocera-services start SteamController2
```

## Logs

```text
/userdata/system/logs/sc2bridge.log
```

Example:

```bash
tail -n 100 /userdata/system/logs/sc2bridge.log
```

## Testing status

Confirmed during development:

- Standard controller input works.
- Extra buttons work.
- Force feedback works.
- Real in-game rumble works through Batocera/Wine.
- Automatic disconnect/reconnect lifecycle works.
- Bluetooth HID identity has been confirmed on a second controller.
- A second Steam Controller 2 has independently passed normal controller-function testing.
- v0.8.0 right-trackpad mouse movement works on the development Steam Deck/Batocera system.
- v0.8.0 left-pad left/right mouse clicks work on the development Steam Deck/Batocera system.
- Mouse filtering substantially reduces the jitter seen with raw coordinate-delta conversion.

Final independent v0.8.0 sanity testing of the new mouse functions is pending.

## Suggested release

Tag:

```text
v0.8.0
```

Release title:

```text
Steam Controller 2 for Batocera v0.8.0
```

Release package contents:

```text
sc2bridge.py
INSTALL.txt
TEST_CHECKLIST.txt
RELEASE_NOTES.txt
```

This is still a pre-1.0 development release. If independent v0.8.0 testing passes cleanly, it is a strong candidate to become the basis for the first stable release.
