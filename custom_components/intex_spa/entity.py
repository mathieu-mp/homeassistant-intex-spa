"""BlueprintEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    NAME,
    VERSION,
    DEFAULT_NAME,
    DEFAULT_PARALLEL_UPDATES,
)

PARALLEL_UPDATES = DEFAULT_PARALLEL_UPDATES


class IntexSpaEntity(CoordinatorEntity):
    """Class to inherit from all Intex Spa entities."""

    def __init__(self, coordinator, entry, icon: str):
        super().__init__(coordinator)
        self.entry = entry
        self._attr_icon = icon

    # @property
    # def unique_id(self):
    #     """Return a unique ID to use for this entity."""
    #     return self.config_entry.entry_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.entry.data.get("name", DEFAULT_NAME))},
            "name": self.entry.data.get("name", DEFAULT_NAME),
            "model": VERSION,
            "manufacturer": NAME,
        }

    # @property
    # def extra_state_attributes(self):
    #     """Return the state attributes."""
    #     return {
    #         "attribution": ATTRIBUTION,
    #         "id": str(self.coordinator.data.get("id")),
    #         "integration": DOMAIN,
    #     }
