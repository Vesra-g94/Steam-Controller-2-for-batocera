# v0.3.0 Expanded Button Support

v0.3.0 expands Steam Controller 2 support by exposing the controller's extra physical buttons as distinct Linux input events that Batocera can assign through its controller and global hotkey configuration.

## Newly exposed buttons

| Steam Controller 2 button | Linux input code |
|---|---|
| QAM | `BTN_TRIGGER_HAPPY1` |
| L4 | `BTN_TRIGGER_HAPPY2` |
| L5 | `BTN_TRIGGER_HAPPY3` |
| R4 | `BTN_TRIGGER_HAPPY4` |
| R5 | `BTN_TRIGGER_HAPPY5` |

These names are only the internal Linux event codes. In documentation and user-facing guidance, the buttons should still be referred to by their actual Steam Controller 2 labels: QAM, L4, L5, R4, and R5.

## Why these input codes are used

Linux does not currently provide native button labels specifically named `QAM`, `L4`, `L5`, `R4`, or `R5` for this controller.

The bridge therefore uses unused `BTN_TRIGGER_HAPPY*` codes so the buttons remain:

- distinct
- non-conflicting with standard gamepad controls
- visible to Batocera
- individually assignable by the user

## Verified mapping

The following raw button masks were previously identified from the Steam Controller 2 Bluetooth HID report:

```text
QAM  0x00000010
R4   0x00000080
R5   0x00000100
L4   0x00020000
L5   0x00040000
```

v0.3.0 exposes them as:

```text
QAM -> BTN_TRIGGER_HAPPY1
L4  -> BTN_TRIGGER_HAPPY2
L5  -> BTN_TRIGGER_HAPPY3
R4  -> BTN_TRIGGER_HAPPY4
R5  -> BTN_TRIGGER_HAPPY5
```

## evtest validation

All five buttons were confirmed to generate clean press/release events through the virtual controller:

```text
BTN_TRIGGER_HAPPY1
BTN_TRIGGER_HAPPY2
BTN_TRIGGER_HAPPY3
BTN_TRIGGER_HAPPY4
BTN_TRIGGER_HAPPY5
```

Each event produced a normal:

```text
value 1
```

on press and:

```text
value 0
```

on release.

## Batocera validation

Batocera successfully detected all five extra inputs from:

```text
Vesra Steam Controller 2 Bridge
```

and exposed them as assignable global hotkey inputs.

Observed entries included:

```text
BTN_TRIGGER_HAPPY1
BTN_TRIGGER_HAPPY2
BTN_TRIGGER_HAPPY3
BTN_TRIGGER_HAPPY4
BTN_TRIGGER_HAPPY5
```

The buttons were successfully assigned to Batocera actions such as:

- Coin
- Save State
- Overlays
- Brightness Cycle

This confirms that the extra SC2 buttons can be used as normal user-configurable Batocera hotkeys.

## Current v0.3.0 status

Expanded button support:

- QAM — working
- L4 — working
- L5 — working
- R4 — working
- R5 — working

Existing v0.2.1 functionality remains unchanged:

- standard gamepad controls
- automatic Bluetooth reconnect
- automatic bridge start/stop
- no ghost controller while SC2 is off
- stale Bluetooth recovery after repeated reconnect failures

## Still not implemented

The following remain future targets:

- trackpads
- gyroscope
- rumble / haptics
