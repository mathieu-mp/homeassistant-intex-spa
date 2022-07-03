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
    intex_spa = IntexSpa(data["host"])
    try:
        await intex_spa.async_update_status()

    except IntexSpaDnsException as err:
        raise DnsNotKnown from err

    except Exception as err:
        raise CannotConnect from err

    # Return info that you want to store in the config entry.
    return {"title": data["name"]}


class IntexSpaMainFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Main config flow for IntexSpa."""

    VERSION = 1
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
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except DnsNotKnown:
            errors["host"] = "dns_not_known"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_MAIN_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class DnsNotKnown(HomeAssistantError):
    """Error to indicate there is invalid auth."""
