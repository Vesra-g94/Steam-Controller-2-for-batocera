# Steam Controller 2 for Batocera — v0.5.0 Repo Update

## v0.5.0 — Rumble / Force Feedback

This update adds working force feedback support for the Steam Controller 2 Bluetooth bridge on Batocera.

The bridge now exposes Linux `FF_RUMBLE` through the virtual controller and translates game/emulator rumble requests into Steam Controller 2 Bluetooth HID output reports.

## What changed

### Force Feedback
- Added `FF_RUMBLE` capability to the virtual controller.
- Added support for force-feedback effect upload, play, stop, and erase.
- Added translation from Linux strong/weak rumble magnitudes to Steam Controller 2 haptic output.
- Uses Steam Controller 2 output report `0x80`.
- Uses independently addressable left and right haptic channels.
- Uses a tested practical gain range of `1..128`.
- Zero rumble requests send a true stop packet so the controller does not retain a light baseline vibration.

### Existing functionality retained
- Standard buttons
- D-pad
- Analog sticks
- Analog triggers
- QAM
- L4 / L5
- R4 / R5
- Left trackpad analog X/Y
- Right trackpad analog X/Y
- Trackpad touch gating
- Trackpad axes reset to center on release
- Bluetooth reconnect watcher
- Bluetooth recovery after repeated reconnect failures
- Fallback keyboard/mouse interface grabbing

## Force Feedback Validation

The following behavior has been confirmed during development:

- Virtual controller advertises `FF_RUMBLE`.
- Linux FF effect upload succeeds.
- Strong and weak magnitudes are received by the bridge.
- FF play events start controller haptics.
- FF stop events stop controller haptics.
- FF erase removes the effect cleanly.
- Left and right haptic channels can be driven independently.
- Gain increases progressively through the usable range.
- Gain `128` was the strongest useful tested value.
- Values above `128` became weaker and/or asymmetric, so the bridge caps the practical range at `128`.
- Controller sleep/reconnect recreated the bridge with force feedback still available.
- Real in-game rumble was successfully confirmed in a Windows game running through Batocera/Wine.

## Steam Controller 2 Haptic Report

Bluetooth HID output report used for rumble:

```text
Report ID: 0x80
Total packet size: 10 bytes
```

Current bridge packet layout:

```text
0x80
type
intensity (u16 LE)
left_speed (u16 LE)
left_gain (u8)
right_speed (u16 LE)
right_gain (u8)
```

The current implementation uses:

```text
HAPTIC_SPEED = 18000
HAPTIC_MAX_GAIN = 128
```

Linux rumble magnitudes are scaled from:

```text
0..65535
```

to:

```text
0 = true stop
1..65535 = gain 1..128
```

## Trackpad Support from v0.4.0

Trackpads remain exposed as analog axes:

```text
Left pad:
X -> ABS_HAT1X
Y -> ABS_HAT1Y

Right pad:
X -> ABS_HAT2X
Y -> ABS_HAT2Y
```

Trackpad click is intentionally not exposed as an additional button to reduce accidental clicks while using the pads as analog controls.

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

The bridge auto-detects the controller by HID identity and does not depend on a fixed `/dev/hidrawX` number.

## Install Paths

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

Or start it manually over SSH:

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

## Testing Status

v0.5.0 has passed development testing for:
- standard controller input
- expanded buttons
- dual analog trackpads
- Bluetooth reconnect
- force-feedback upload/play/stop/erase
- real in-game rumble

Additional independent testing is encouraged before treating the release as fully validated across more Batocera systems, Bluetooth adapters, controller units, and games.

## Suggested Release

Tag:

```text
v0.5.0
```

Release title:

```text
Steam Controller 2 for Batocera v0.5.0
```
