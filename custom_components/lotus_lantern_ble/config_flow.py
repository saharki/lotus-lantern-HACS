import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_ADDRESS, CONF_NAME

CONF_CHAR_UUID = "char_uuid"

@config_entries.HANDLERS.register(DOMAIN)
class LotusLanternBleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Lotus Lantern BLE."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # TODO: Optionally validate BLE address and char UUID format
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default="Lotus Lantern BLE Light"): str,
                vol.Required(CONF_ADDRESS): str,
                vol.Required(CONF_CHAR_UUID, default="0000fff3-0000-1000-8000-00805f9b34fb"): str,
            }),
            errors=errors,
        )

    # TODO: Support adding multiple devices in one flow 