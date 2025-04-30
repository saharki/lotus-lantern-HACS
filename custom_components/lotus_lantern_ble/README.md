# Lotus Lantern BLE

Custom Home Assistant integration for controlling Lotus Lantern BLE LED strips.

## Features

- RGB color control
- Multiple device support
- Brightness control (scales RGB values)

## Example configuration.yaml

# Multiple devices:

```yaml
light:
  - platform: lotus_lantern_ble
    devices:
      - name: "Lotus Lantern Strip 1"
        address: "BE:27:08:00:32:5F"
      - name: "Lotus Lantern Strip 2"
        address: "BE:27:08:00:32:60"
    # Brightness is supported via Home Assistant UI or service calls
```

# Single device (backward compatible):

```yaml
light:
  - platform: lotus_lantern_ble
    name: "Lotus Lantern Strip"
    address: "BE:27:08:00:32:5F"
```

## Notes

- Brightness is handled by scaling the RGB values sent to the device.
- Setting brightness to 0 is equivalent to turning the light off.
