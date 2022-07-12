"""BlueprintEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from . import IntexSpaDataUpdateCoordinator

from .const import (
    DOMAIN,
    NAME,
    # VERSION,
    DEFAULT_NAME,
    DEFAULT_PARALLEL_UPDATES,
)

PARALLEL_UPDATES = DEFAULT_PARALLEL_UPDATES


class IntexSpaEntity(CoordinatorEntity):
    """Class to inherit from all Intex Spa entities."""

    def __init__(
        self,
        coordinator: IntexSpaDataUpdateCoordinator,
        entry: ConfigEntry,
        icon: str,
    ):
        super().__init__(coordinator)
        self.entry = entry
        self._attr_icon = icon

    @property
    def device_info(self):
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (
                    DOMAIN,
                    self.entry.data["info"]["uid"],
                )
            },
            "name": self.entry.data.get("name", DEFAULT_NAME),
            "model": self.entry.data["info"]["uid"],
            "manufacturer": NAME,
        }

    @property
    def available(self):
        if not self.coordinator.last_update_success:
            return False
        elif self.coordinator.data.error_code is False:
            return True
        else:
            return False
