"""Climate platform for Intex Spa integration."""

from homeassistant.components.climate import ClimateEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.const import (
    ATTR_TEMPERATURE,
    UnitOfTemperature,
)
from homeassistant.components.climate.const import (
    HVACMode,
    ClimateEntityFeature,
)

from .entity import IntexSpaEntity
from . import IntexSpaDataUpdateCoordinator
from .const import (
    DOMAIN,
    DEFAULT_NAME,
    PARALLEL_UPDATES_DISABLED,
)

PARALLEL_UPDATES = PARALLEL_UPDATES_DISABLED


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add switches for passed entry in HA."""
    coordinator: IntexSpaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            IntexSpaClimate(
                coordinator,
                entry,
                icon="mdi:pool-thermometer",
            )
        ]
    )


class IntexSpaClimate(IntexSpaEntity, ClimateEntity):
    """Intex Spa climate class."""

    _attr_hvac_modes = [
        HVACMode.HEAT,
        HVACMode.OFF,
    ]
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
    _attr_target_temperature_step = 1

    def __init__(
        self,
        coordinator: IntexSpaDataUpdateCoordinator,
        entry: ConfigEntry,
        icon: str,
    ):
        """Initilize an IntexSpaClimate with an IntexSpaDataUpdateCoordinator and ConfigEntry."""
        super().__init__(coordinator, entry, icon)

        self._attr_name = self.entry.data.get("name", DEFAULT_NAME)
        self._attr_unique_id = self.entry.entry_id

    @property
    def temperature_unit(self):
        """Return the unit of measurement of this entity."""
        return self.coordinator.data.unit

    @property
    def current_temperature(self):
        """Return the state of the sensor."""
        return self.coordinator.data.current_temp

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        if self.temperature_unit == UnitOfTemperature.CELSIUS:
            return 20
        else:
            return 50

    @property
    def max_temp(self):
        """Return the maximum temperature.."""
        if self.temperature_unit == UnitOfTemperature.CELSIUS:
            return 40
        else:
            return 104

    @property
    def target_temperature(self):
        """Return the state of the sensor."""
        return self.coordinator.data.preset_temp

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        status = await self.coordinator.api.async_set_preset_temp(
            int(kwargs.get(ATTR_TEMPERATURE))
        )
        self.coordinator.async_set_updated_data(status)

    @property
    def hvac_mode(self):
        """Return current operation ie. heat, off..."""
        if self.coordinator.data.heater:
            return HVACMode.HEAT

        return HVACMode.OFF

    async def async_set_hvac_mode(self, hvac_mode):
        """Set HVAC mode."""
        if hvac_mode == HVACMode.OFF:
            status = await self.coordinator.api.async_set_heater(False)
            self.coordinator.async_set_updated_data(status)
            return

        if hvac_mode == HVACMode.HEAT:
            status = await self.coordinator.api.async_set_heater(True)
            self.coordinator.async_set_updated_data(status)
            return
