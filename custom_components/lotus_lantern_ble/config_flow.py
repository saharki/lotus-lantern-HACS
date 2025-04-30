import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_ADDRESS, CONF_NAME, CONF_DEVICES

CONF_CHAR_UUID = "char_uuid"

@config_entries.HANDLERS.register(DOMAIN)
class LotusLanternBleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Lotus Lantern BLE."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Expect a list of devices
            devices = user_input[CONF_DEVICES]
            return self.async_create_entry(title="Lotus Lantern BLE Devices", data={CONF_DEVICES: devices})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_DEVICES): vol.All(
                    [
                        {
                            vol.Required(CONF_NAME): str,
                            vol.Required(CONF_ADDRESS): str,
                            vol.Required(CONF_CHAR_UUID, default="0000fff3-0000-1000-8000-00805f9b34fb"): str,
                        }
                    ]
                )
            }),
            errors=errors,
        )

    # TODO: Support adding multiple devices in one flow 