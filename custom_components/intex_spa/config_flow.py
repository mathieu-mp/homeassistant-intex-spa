"""Adds config flow for Intex Spa Integration."""
# Standard
import logging
from typing import Any

# Home Assistant
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

# Custom Integration
from intex_spa import IntexSpa, IntexSpaDnsException
from .const import (
    STEP_USER_MAIN_SCHEMA,
    DOMAIN,
)

_LOGGER: logging.Logger = logging.getLogger(__name__)


async def validate_input(
    hass: HomeAssistant, data: dict[str, Any]  # pylint: disable=unused-argument
) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_MAIN_SCHEMA with values provided by the user.
    """
    try:
        intex_spa = IntexSpa(data["host"])
        info = await intex_spa.async_update_info()

    except IntexSpaDnsException as err:
        raise DnsNotKnown from err

    except Exception as err:
        raise CannotConnect from err

    else:
        # Return data to store in the config entry.
        return data, info.uid


class IntexSpaMainFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Main config flow for IntexSpa."""

    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(
        self,
        user_input: dict[str, Any] = None,
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_MAIN_SCHEMA
            )

        errors = {}

        try:
            validated_data, device_unique_id = await validate_input(
                self.hass, user_input
            )
        except CannotConnect:
            errors["host"] = "cannot_connect"
        except DnsNotKnown:
            errors["host"] = "dns_not_known"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            # Set a unique identifier for this config flow and abort if already configured
            await self.async_set_unique_id(device_unique_id)
            self._abort_if_unique_id_configured()

            # Create the entry with the return values from validate_input
            return self.async_create_entry(
                title=validated_data["name"],
                data=validated_data,
            )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_MAIN_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class DnsNotKnown(HomeAssistantError):
    """Error to indicate there is invalid auth."""
