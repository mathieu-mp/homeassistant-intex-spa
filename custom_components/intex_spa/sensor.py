"""Switch platform for intex_spa."""
from homeassistant.components.sensor import SensorEntity

# from homeassistant.components. import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import EntityCategory


from .entity import IntexSpaEntity
from . import IntexSpaDataUpdateCoordinator
from .const import (
    DEFAULT_NAME,
    DOMAIN,
    DEFAULT_PARALLEL_UPDATES,
)

PARALLEL_UPDATES = DEFAULT_PARALLEL_UPDATES


# This function is called as part of the __init__.async_setup_entry (via the
# hass.config_entries.async_forward_entry_setup call)
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add switches for passed entry in HA."""
    coordinator: IntexSpaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            IntexSpaSensor(
                coordinator,
                entry,
                icon="mdi:alert-circle-outline",
            ),
        ]
    )


class IntexSpaSensor(IntexSpaEntity, SensorEntity):
    """Intex Spa generic switch class."""

    def __init__(
        self,
        coordinator: IntexSpaDataUpdateCoordinator,
        entry,
        icon: str,
    ):
        super().__init__(coordinator, entry, icon)

        self._attr_name = "{0} Error".format(
            self.entry.data.get("name", DEFAULT_NAME),
        )
        self._attr_unique_id = "{0}_error_code".format(
            self.entry.entry_id,
        )
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        if not self.coordinator.data.error_code is False:
            return self.coordinator.data.error_code
        else:
            return "None"

    # Redefine the super class 'available' property
    @property
    def available(self):
        return True
