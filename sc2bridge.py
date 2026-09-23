#!/usr/bin/env python3

import os
import glob
import struct
from evdev import UInput, InputDevice, ecodes as e, AbsInfo, list_devices

VIDPID = "0005:000028DE:00001303"
STICK_DEADZONE = 1800


def grab_fallback_interfaces():
    grabbed = []

    for path in list_devices():
        try:
            dev = InputDevice(path)

            if (
                "Steam Ctrl (BT)" in dev.name
                and (
                    "Keyboard" in dev.name
                    or "Mouse" in dev.name
                )
            ):
                dev.grab()
                grabbed.append(dev)
                print(f"Grabbed fallback interface: {dev.path} - {dev.name}")

        except Exception:
            pass

    return grabbed


def find_controller():
    for path in glob.glob("/sys/class/hidraw/hidraw*/device/uevent"):
        try:
            with open(path, "r") as f:
                text = f.read()

            if f"HID_ID={VIDPID}" in text:
                hid = path.split("/")[4]
                return "/dev/" + hid

        except Exception:
            pass

    return None


def s16(buf, off):
    return struct.unpack_from("<h", buf, off)[0]


def u16(buf, off):
    return struct.unpack_from("<H", buf, off)[0]


def u32(buf, off):
    return struct.unpack_from("<I", buf, off)[0]


def deadzone(v):
    return 0 if abs(v) < STICK_DEADZONE else v


hidraw = find_controller()

if not hidraw:
    print("Steam Controller 2 Bluetooth device 28DE:1303 not found.")
    raise SystemExit(1)

print(f"Steam Controller 2 found: {hidraw}")

grabbed_devices = grab_fallback_interfaces()

cap = {
    e.EV_KEY: [
        e.BTN_SOUTH,       # A
        e.BTN_EAST,        # B
        e.BTN_WEST,        # X
        e.BTN_NORTH,       # Y

        e.BTN_TL,          # LB
        e.BTN_TR,          # RB

        e.BTN_THUMBL,      # L3
        e.BTN_THUMBR,      # R3

        e.BTN_SELECT,      # View
        e.BTN_START,       # Menu
        e.BTN_MODE,        # Steam

        e.BTN_DPAD_UP,
        e.BTN_DPAD_DOWN,
        e.BTN_DPAD_LEFT,
        e.BTN_DPAD_RIGHT,
    ],

    e.EV_ABS: [
        (e.ABS_X,  AbsInfo(0, -32768, 32767, 1800, 128, 0)),
        (e.ABS_Y,  AbsInfo(0, -32768, 32767, 1800, 128, 0)),
        (e.ABS_RX, AbsInfo(0, -32768, 32767, 1800, 128, 0)),
        (e.ABS_RY, AbsInfo(0, -32768, 32767, 1800, 128, 0)),

        (e.ABS_Z,  AbsInfo(0, 0, 32767, 0, 0, 0)),
        (e.ABS_RZ, AbsInfo(0, 0, 32767, 0, 0, 0)),
    ],
}

ui = UInput(
    cap,
    name="Vesra Steam Controller 2 Bridge",
    vendor=0x28de,
    product=0x1303,
    version=1
)

BUTTONS = {
    0x00000001: e.BTN_SOUTH,    # A
    0x00000002: e.BTN_EAST,     # B
    0x00000004: e.BTN_WEST,     # X
    0x00000008: e.BTN_NORTH,    # Y

    0x00080000: e.BTN_TL,       # LB
    0x00000200: e.BTN_TR,       # RB

    0x00008000: e.BTN_THUMBL,   # L3
    0x00000020: e.BTN_THUMBR,   # R3

    0x00000040: e.BTN_SELECT,    # View
    0x00004000: e.BTN_START,     # Menu
    0x00010000: e.BTN_MODE,      # Steam
}

fd = os.open(hidraw, os.O_RDONLY)

print("Virtual controller created:")
print("  Vesra Steam Controller 2 Bridge")
print()
print("Bridge running. Ctrl+C to stop.")
print()

try:
    while True:
        data = os.read(fd, 64)

        if len(data) < 46 or data[0] != 0x45:
            continue

        buttons = u32(data, 2)

        lt = u16(data, 6)
        rt = u16(data, 8)

        lx = deadzone(s16(data, 10))
        ly = deadzone(s16(data, 12))
        rx = deadzone(s16(data, 14))
        ry = deadzone(s16(data, 16))

        for mask, code in BUTTONS.items():
            ui.write(e.EV_KEY, code, 1 if buttons & mask else 0)

        ui.write(e.EV_KEY, e.BTN_DPAD_UP,    1 if buttons & 0x00002000 else 0)
        ui.write(e.EV_KEY, e.BTN_DPAD_DOWN,  1 if buttons & 0x00000400 else 0)
        ui.write(e.EV_KEY, e.BTN_DPAD_LEFT,  1 if buttons & 0x00001000 else 0)
        ui.write(e.EV_KEY, e.BTN_DPAD_RIGHT, 1 if buttons & 0x00000800 else 0)

        ui.write(e.EV_ABS, e.ABS_X, lx)
        ui.write(e.EV_ABS, e.ABS_Y, ly)
        ui.write(e.EV_ABS, e.ABS_RX, rx)
        ui.write(e.EV_ABS, e.ABS_RY, ry)
        ui.write(e.EV_ABS, e.ABS_Z, lt)
        ui.write(e.EV_ABS, e.ABS_RZ, rt)

        ui.syn()

except KeyboardInterrupt:
    print("\nStopping Steam Controller 2 bridge.")

finally:
    os.close(fd)
    ui.close()

    for dev in grabbed_devices:
        try:
            dev.ungrab()
        except Exception:
            pass
