import logging
import asyncio
from homeassistant.components.light import (
    ATTR_RGB_COLOR, ATTR_BRIGHTNESS, LightEntity, SUPPORT_RGB, SUPPORT_BRIGHTNESS
)
from homeassistant.const import CONF_NAME
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, CONF_ADDRESS, CONF_DEVICES

CONF_CHAR_UUID = "char_uuid"

_LOGGER = logging.getLogger(__name__)

# TODO: Support more config options

def build_rgb_payload(r, g, b):
    return bytearray([0x7e, 0x07, 0x05, 0x03, r, g, b, 0x00, 0xef])

async def async_set_color(address, char_uuid, r, g, b):
    try:
        from bleak import BleakClient, BleakError
        async with BleakClient(address) as client:
            await client.write_gatt_char(char_uuid, build_rgb_payload(r, g, b))
        return True
    except Exception as e:
        _LOGGER.error(f"BLE error: {e}")
        return False

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    devices = config.get(CONF_DEVICES)
    entities = []
    if devices:
        for device in devices:
            name = device.get(CONF_NAME, "Lotus Lantern BLE Light")
            address = device.get(CONF_ADDRESS)
            char_uuid = device.get(CONF_CHAR_UUID)
            if address and char_uuid:
                entities.append(LotusLanternBleLight(name, address, char_uuid))
    async_add_entities(entities)

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    # Setup from config flow (UI)
    devices = entry.data.get(CONF_DEVICES)
    entities = []
    if devices:
        for device in devices:
            name = device.get(CONF_NAME, "Lotus Lantern BLE Light")
            address = device.get(CONF_ADDRESS)
            char_uuid = device.get(CONF_CHAR_UUID)
            if address and char_uuid:
                entities.append(LotusLanternBleLight(name, address, char_uuid))
    async_add_entities(entities)

class LotusLanternBleLight(LightEntity):
    def __init__(self, name, address, char_uuid):
        self._name = name
        self._address = address
        self._char_uuid = char_uuid
        self._is_on = False
        self._rgb_color = (255, 255, 255)
        self._brightness = 255

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    @property
    def supported_features(self):
        return SUPPORT_RGB | SUPPORT_BRIGHTNESS

    @property
    def rgb_color(self):
        return self._rgb_color

    @property
    def brightness(self):
        return self._brightness

    async def async_turn_on(self, **kwargs):
        rgb = kwargs.get(ATTR_RGB_COLOR, self._rgb_color)
        brightness = kwargs.get(ATTR_BRIGHTNESS, self._brightness)
        # Scale RGB by brightness
        r = int(rgb[0] * brightness / 255)
        g = int(rgb[1] * brightness / 255)
        b = int(rgb[2] * brightness / 255)
        success = await async_set_color(self._address, self._char_uuid, r, g, b)
        if success:
            self._is_on = True
            self._rgb_color = rgb
            self._brightness = brightness
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        # Turn off by setting color to (0,0,0)
        success = await async_set_color(self._address, self._char_uuid, 0, 0, 0)
        if success:
            self._is_on = False
            self.async_write_ha_state() 