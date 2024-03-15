"""Custom integration to integrate Intex Spa with Home Assistant.

For more details about this integration, please refer to
https://github.com/mathieu-mp/homeassistant-intex-spa
"""

from __future__ import annotations


import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from aio_intex_spa import IntexSpa, IntexSpaUnreachableException, IntexSpaDnsException
from .const import (
    DOMAIN,
    PLATFORMS,
    SCAN_INTERVAL,
    STARTUP_MESSAGE,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(
    hass: HomeAssistant, config: Config  # pylint: disable=unused-argument
) -> bool:
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    api = IntexSpa(entry.data["host"])
    coordinator = IntexSpaDataUpdateCoordinator(hass, api=api)
    await coordinator.async_config_entry_first_refresh()
    await coordinator.async_update_info()
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


class IntexSpaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, api: IntexSpa) -> None:
        """Initialize."""
        self.api: IntexSpa = api
        self.platforms = []
        self.info = {}

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via intex-spa python library."""
        try:
            return await self.api.async_update_status()
        except (IntexSpaUnreachableException, IntexSpaDnsException) as exception:
            raise UpdateFailed(exception) from exception
        except Exception as exception:
            raise NotImplementedError from exception

    async def async_update_info(self):
        """Update info via intex-spa python library."""
        try:
            self.info = await self.api.async_update_info()
        except (IntexSpaUnreachableException, IntexSpaDnsException) as exception:
            raise UpdateFailed(exception) from exception
        except Exception as exception:
            raise NotImplementedError from exception


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
