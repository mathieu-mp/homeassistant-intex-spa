"""IntexSpaEntity class."""

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from . import IntexSpaDataUpdateCoordinator

from .const import (
    DOMAIN,
    NAME,
    DEFAULT_NAME,
    PARALLEL_UPDATES_DISABLED,
)

PARALLEL_UPDATES = PARALLEL_UPDATES_DISABLED


class IntexSpaEntity(CoordinatorEntity):
    """Class to inherit from all Intex Spa entities."""

    def __init__(
        self,
        coordinator: IntexSpaDataUpdateCoordinator,
        entry: ConfigEntry,
        icon: str,
        is_enabled_by_default: bool = True,
    ):
        """Initialize an IntexSpaEntity with a IntexSpaDataUpdateCoordinator and a ConfigEntry."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_icon = icon
        self._attr_entity_registry_enabled_default = is_enabled_by_default

    @property
    def device_info(self) -> DeviceInfo:
        """Return the properties of the device as a DeviceInfo."""
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (
                    DOMAIN,
                    self.coordinator.info.uid,
                )
            },
            "name": self.entry.data.get("name", DEFAULT_NAME),
            "model": self.entry.data.get("name", DEFAULT_NAME),
            "manufacturer": NAME,
        }

    @property
    def available(self) -> bool:
        """Return the availability state of the connection to the device, as a bool."""

        if not self.coordinator.last_update_success:
            return False
        elif self.coordinator.data.error_code is False:
            return True
        else:
            return False
