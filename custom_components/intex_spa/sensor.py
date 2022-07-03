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
            IntexSpaErrorSensor(
                coordinator,
                entry,
                icon="mdi:alert-circle-outline",
                name="Error",
                entity="error",
            ),
            IntexSpaErrorSensor(
                coordinator,
                entry,
                icon="mdi:alert-circle-outline",
                name="Error Description",
                entity="error_description",
            ),
            IntexSpaErrorSensor(
                coordinator,
                entry,
                icon="mdi:alert-circle-outline",
                name="Error Code",
                entity="error_code",
                enabled_by_default=False,
            ),
        ]
    )


class IntexSpaErrorSensor(IntexSpaEntity, SensorEntity):
    """Intex Spa generic switch class."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: IntexSpaDataUpdateCoordinator,
        entry,
        icon: str,
        name: str,
        entity: str,
        enabled_by_default: bool = True,
    ):
        super().__init__(coordinator, entry, icon)

        name_or_default_name = self.entry.data.get("name", DEFAULT_NAME)
        self._attr_name = f"{name_or_default_name} {name}"
        self._attr_unique_id = f"{self.entry.entry_id}_{entity}"
        self._attr_device_class = f"intex_spa__{entity}"
        self._attr_entity_registry_enabled_default = enabled_by_default

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        if not self.coordinator.data.error_code is False:
            return self.coordinator.data.error_code
        else:
            return "None"

    # Redefine the super class IntexSpaEntity 'available' property
    @property
    def available(self):
        return self.coordinator.last_update_success

    @property
    def icon(self):
        if not self.coordinator.data.error_code is False:
            return "mdi:alert-circle-outline"
        else:
            return "mdi:alert-circle-check-outline"
