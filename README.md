# Steam Controller 2 for Batocera — v0.2.0 Test Data

This document records the compatibility and behavior observed while developing
v0.2.0 of the Steam Controller 2 userspace bridge for Batocera.

## Bluetooth HID Identity

Two separate Steam Controller 2 units were checked independently.

Both reported:

```text
Bus=0005
Vendor=28de
Product=1303
Version=0100
HID_ID=0005:000028DE:00001303
DRIVER=hid-generic
```

The per-controller values were different, as expected:

- `HID_UNIQ` / Bluetooth MAC address
- `HID_NAME` serial-like suffix
- `/dev/hidrawX` number
- `/dev/input/eventXX` numbers

The bridge therefore identifies the controller by:

```text
28DE:1303
```

rather than by a hard-coded `hidraw` or `event` number.

## Native Batocera Exposure

Before the bridge is active, the Steam Controller 2 is exposed by Batocera as
Bluetooth keyboard and mouse fallback interfaces.

Observed examples:

```text
Steam Ctrl (BT) ... Mouse
Steam Ctrl (BT) ... Keyboard
```

The bridge temporarily grabs those fallback interfaces while it is active so
they do not interfere with Batocera controller mapping.

## Virtual Gamepad

When the bridge is active, Linux exposes:

```text
Name="Vesra Steam Controller 2 Bridge"
Phys=py-evdev-uinput
```

Observed handlers included:

```text
eventXX
js3
```

The exact event number changes between sessions and is not hard-coded.

## Standard Controls Verified

The following controls were verified through the userspace bridge:

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

The D-pad is exposed as digital gamepad buttons.

## Raw Button Bit Mapping

Verified button masks:

```text
A           0x00000001
B           0x00000002
X           0x00000004
Y           0x00000008

QAM         0x00000010
R3          0x00000020
View        0x00000040
R4          0x00000080
R5          0x00000100
RB          0x00000200

D-pad Down  0x00000400
D-pad Right 0x00000800
D-pad Left  0x00001000
D-pad Up    0x00002000

Menu        0x00004000
L3          0x00008000
Steam       0x00010000
L4          0x00020000
L5          0x00040000
LB          0x00080000
```

Additional higher-order state bits were observed for touch/click/grip states,
but those features are not yet exposed by v0.2.0.

## Analog Report Layout

The bridge currently decodes the `0x45` HID report as:

```text
buttons = u32(data, 2)

LT = u16(data, 6)
RT = u16(data, 8)

LX = s16(data, 10)
LY = s16(data, 12)
RX = s16(data, 14)
RY = s16(data, 16)
```

Observed trigger range:

```text
0 .. 32767
```

Observed stick range:

```text
approximately -32768 .. 32767
```

A software dead zone of `1800` is currently applied to the four stick axes.

## v0.2.0 Lifecycle Test

The following sequence was validated on Batocera v43:

### 1. Controller powered off

Result:

```text
sc2watcher.sh running
sc2bridge.py not running
no Vesra virtual controller present
```

PASS

### 2. Controller powered on

The watcher detected the paired controller, allowed the Bluetooth/HID connection
to settle, and started the bridge.

Observed log:

```text
Allowing SC2 connection to settle.
Steam Controller 2 connection is stable.
Starting Steam Controller 2 bridge.
```

The virtual controller appeared successfully.

PASS

### 3. Controller powered off again

The raw HID device disappeared, the bridge exited, and the virtual gamepad was
removed.

The watcher remained running.

PASS

### 4. Controller powered back on

The watcher automatically restored the Bluetooth connection, waited for the HID
interface, and restarted the bridge.

Observed state:

```text
Connected: yes
```

and the virtual controller reappeared.

PASS

## Reconnect Issue Found During Development

An earlier watcher revision repeatedly issued `bluetoothctl connect` while the
Bluetooth connection was still initializing.

This produced errors such as:

```text
org.bluez.Error.Failed le-connection-abort-by-local
```

The final v0.2.0 watcher avoids that behavior by separating the connection state
into stages:

```text
Disconnected
    -> request Bluetooth connection

Bluetooth connected but HID not ready
    -> wait; do not issue another connection request

Bluetooth connected + HID present
    -> allow settle delay
    -> start bridge
```

That state handling produced a successful off/on/off/reconnect cycle.

## Compatibility Status

Confirmed so far:

- 2 separate Steam Controller 2 units report Bluetooth HID `28DE:1303`
- Batocera exposes the same keyboard/mouse fallback structure on the independently tested controller
- v0.2.0 automatic bridge lifecycle was validated on Batocera v43

This is encouraging compatibility data, but it is not yet proof of universal
compatibility across every Steam Controller 2 firmware revision or every
Batocera hardware platform.

## Features Not Yet Validated / Implemented

- QAM as a mapped gamepad control
- L4 / L5 / R4 / R5 rear buttons
- Trackpads
- Gyroscope
- Rumble / haptics

These remain future development targets.
