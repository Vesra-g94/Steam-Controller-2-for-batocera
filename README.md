# Steam Controller 2 for Batocera

Userspace Bluetooth bridge for the **Steam Controller 2** on Batocera.

## v0.4.0

v0.4.0 adds usable analog support for both Steam Controller 2 trackpads while retaining the extra-button support from v0.3.0 and the reconnect/recovery behavior from v0.2.1.

### Trackpad mapping

| SC2 control | Linux input code |
|---|---|
| Left trackpad X | `ABS_HAT1X` |
| Left trackpad Y | `ABS_HAT1Y` |
| Right trackpad X | `ABS_HAT2X` |
| Right trackpad Y | `ABS_HAT2Y` |

Trackpad output is **touch-gated**. While a pad is touched, its raw X/Y position is forwarded to the virtual controller. When the finger is lifted, both axes return to `0`.

Trackpad click is intentionally **not** exposed as an additional virtual button in v0.4.0. This avoids accidental button presses while moving across the pads and keeps the already-large button set manageable.

## Verified trackpad report layout

```text
Left pad touch   0x02000000
Left pad click   0x04000000
Left pad X       s16 @ bytes 18-19
Left pad Y       s16 @ bytes 20-21
Left pad pressure u16 @ bytes 22-23

Right pad touch   0x00200000
Right pad click   0x00400000
Right pad X       s16 @ bytes 24-25
Right pad Y       s16 @ bytes 26-27
Right pad pressure u16 @ bytes 28-29
```

Pressure and click state were identified during raw-report testing, but are not exported by the v0.4.0 virtual controller.

## Batocera validation

Both trackpads were confirmed through `evtest` as independent analog X/Y inputs and were accepted by Batocera controller mapping as analog movement.

The virtual device advertises:

```text
ABS_HAT1X
ABS_HAT1Y
ABS_HAT2X
ABS_HAT2Y
```

The axes return to center when touch ends.

## Extra buttons retained from v0.3.0

| SC2 button | Linux input code |
|---|---|
| QAM | `BTN_TRIGGER_HAPPY1` |
| L4 | `BTN_TRIGGER_HAPPY2` |
| L5 | `BTN_TRIGGER_HAPPY3` |
| R4 | `BTN_TRIGGER_HAPPY4` |
| R5 | `BTN_TRIGGER_HAPPY5` |

## Existing reconnect behavior retained

- No ghost virtual controller while the SC2 is off
- Automatic Bluetooth reconnect
- HID readiness wait
- Connection settle delay
- Automatic bridge start/stop/restart
- Bluetooth adapter recovery path after repeated reconnect failures
- Native keyboard/mouse fallback suppression while the bridge is active

## Standard controls working

- A / B / X / Y
- D-pad
- LB / RB
- L3 / R3
- View / Menu / Steam
- Left and right analog sticks
- Left and right analog triggers

## Extra controls working

- QAM
- L4
- L5
- R4
- R5
- Left trackpad analog X/Y
- Right trackpad analog X/Y

## Not yet implemented

- Rumble / haptics
- Gyroscope (optional / future)

## Requirements

- Batocera v43
- Steam Controller 2 paired and trusted over Bluetooth
- Python 3
- `python-evdev`
- Linux `uinput`
- BlueZ / `bluetoothctl`

## Installation

```text
sc2bridge.py              -> /userdata/system/sc2bridge.py
sc2watcher.sh             -> /userdata/system/sc2watcher.sh
services/SteamController2 -> /userdata/system/services/SteamController2
```

Then:

```bash
chmod 755 /userdata/system/sc2bridge.py
chmod 755 /userdata/system/sc2watcher.sh
chmod 755 /userdata/system/services/SteamController2
```

Enable from Batocera:

```text
MAIN MENU -> SYSTEM SETTINGS -> SERVICES -> SteamController2
```

Or via SSH:

```bash
batocera-services start SteamController2
```

## Upgrade from v0.3.0

Only `sc2bridge.py` changed for v0.4.0.

Replace:

```text
/userdata/system/sc2bridge.py
```

Then:

```bash
chmod 755 /userdata/system/sc2bridge.py
batocera-services restart SteamController2
```

## Log

```text
/userdata/system/logs/sc2bridge.log
```

## License

MIT.
