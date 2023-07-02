"""Switch platform for intex_spa."""
from homeassistant.components.sensor import SensorEntity

# from homeassistant.components. import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import EntityCategory

from homeassistant.const import (
    DEVICE_CLASS_TEMPERATURE,
)

from .entity import IntexSpaEntity
from . import IntexSpaDataUpdateCoordinator
from .const import (
    DEFAULT_NAME,
    DOMAIN,
    PARALLEL_UPDATES_DISABLED,
)

PARALLEL_UPDATES = PARALLEL_UPDATES_DISABLED


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
            IntexSpaCurrentTemperatureSensor(
                coordinator,
                entry,
                icon="mdi:pool-thermometer",
                is_enabled_by_default=False,
            ),
            IntexSpaTargetTemperatureSensor(
                coordinator,
                entry,
                icon="mdi:pool-thermometer",
                is_enabled_by_default=False,
            ),
            IntexSpaUidSensor(
                coordinator,
                entry,
                icon="mdi:identifier",
                is_enabled_by_default=False,
            ),
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
                is_enabled_by_default=False,
            ),
        ]
    )


class IntexSpaCurrentTemperatureSensor(IntexSpaEntity, SensorEntity):
    """Intex Spa current temperature sensor class."""

    def __init__(
        self,
        coordinator: IntexSpaDataUpdateCoordinator,
        entry: ConfigEntry,
        icon: str,
        is_enabled_by_default: bool = True,
    ):
        super().__init__(coordinator, entry, icon, is_enabled_by_default)

        name_or_default_name = self.entry.data.get("name", DEFAULT_NAME)
        self._attr_device_class = DEVICE_CLASS_TEMPERATURE
        self._attr_name = f"{name_or_default_name} Current Temperature"
        self._attr_unique_id = f"{self.entry.entry_id}_current_temperature"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self.coordinator.data.current_temp

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement of this entity."""
        return self.coordinator.data.unit


class IntexSpaTargetTemperatureSensor(IntexSpaEntity, SensorEntity):
    """Intex Spa target temperature sensor class."""

    def __init__(
        self,
        coordinator: IntexSpaDataUpdateCoordinator,
        entry: ConfigEntry,
        icon: str,
        is_enabled_by_default: bool = True,
    ):
        super().__init__(coordinator, entry, icon, is_enabled_by_default)

        name_or_default_name = self.entry.data.get("name", DEFAULT_NAME)
        self._attr_device_class = DEVICE_CLASS_TEMPERATURE
        self._attr_name = f"{name_or_default_name} Target Temperature"
        self._attr_unique_id = f"{self.entry.entry_id}_target_temperature"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self.coordinator.data.preset_temp

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement of this entity."""
        return self.coordinator.data.unit


class IntexSpaUidSensor(IntexSpaEntity, SensorEntity):
    """Intex Spa UID Sensor class."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: IntexSpaDataUpdateCoordinator,
        entry: ConfigEntry,
        icon: str,
        is_enabled_by_default: bool = True,
    ):
        super().__init__(coordinator, entry, icon, is_enabled_by_default)

        name_or_default_name = self.entry.data.get("name", DEFAULT_NAME)
        self._attr_name = f"{name_or_default_name} UID"
        self._attr_unique_id = f"{self.entry.entry_id}_uid"

        self._attr_native_value = self.coordinator.info.uid

    # Redefine the super class IntexSpaEntity 'available' property
    @property
    def available(self):
        return self.coordinator.last_update_success


class IntexSpaErrorSensor(IntexSpaEntity, SensorEntity):
    """Intex Spa Error Sensor class."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: IntexSpaDataUpdateCoordinator,
        entry: ConfigEntry,
        icon: str,
        name: str,
        entity: str,
        is_enabled_by_default: bool = True,
    ):
        super().__init__(coordinator, entry, icon, is_enabled_by_default)

        name_or_default_name = self.entry.data.get("name", DEFAULT_NAME)
        self._attr_device_class = f"intex_spa__{entity}"
        self._attr_name = f"{name_or_default_name} {name}"
        self._attr_unique_id = f"{self.entry.entry_id}_{entity}"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        if not self.coordinator.data.error_code is False:
            return self.coordinator.data.error_code.lower()
        else:
            return "none"

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
