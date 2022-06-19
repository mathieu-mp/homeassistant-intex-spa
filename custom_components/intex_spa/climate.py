"""Climate platform for Intex Spa integration."""
from homeassistant.components.climate import ClimateEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS
from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE,
)

from .const import (
    DOMAIN,
    DEFAULT_NAME,
)
from .entity import IntexSpaEntity
from . import IntexSpaDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add switches for passed entry in HA."""
    coordinator: IntexSpaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [
            IntexSpaClimate(
                coordinator,
                entry,
                icon="mdi:power-plug-outline",
            )
        ]
    )


class IntexSpaClimate(IntexSpaEntity, ClimateEntity):
    """Intex Spa climate class."""

    _attr_name = "SPA climate"
    _attr_hvac_modes = [
        HVAC_MODE_HEAT,
        HVAC_MODE_OFF,
    ]
    # TODO: Adapt min, max, and units depending on the actual unit of the spa
    _attr_min_temp = 20
    _attr_max_temp = 40
    _attr_supported_features = SUPPORT_TARGET_TEMPERATURE
    _attr_target_temperature_step = 1
    _attr_temperature_unit = TEMP_CELSIUS

    def __init__(
        self,
        coordinator: IntexSpaDataUpdateCoordinator,
        entry,
        icon: str,
    ):
        super().__init__(coordinator, entry, icon)

        self._attr_name = "{0} Climate".format(
            self.entry.data.get("name", DEFAULT_NAME),
        )
        self._attr_unique_id = "{0}_climate".format(
            self.entry.entry_id,
        )

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the state of the sensor."""
        return self.coordinator.data.current_temp

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
        """Return current operation ie. heat, off"""
        if self.coordinator.data.heater:
            return HVAC_MODE_HEAT

        return HVAC_MODE_OFF

    async def async_set_hvac_mode(self, hvac_mode):
        """Set HVAC mode."""
        if hvac_mode == HVAC_MODE_OFF:
            status = await self.coordinator.api.async_set_heater(False)
            self.coordinator.async_set_updated_data(status)
            return

        if hvac_mode == HVAC_MODE_HEAT:
            status = await self.coordinator.api.async_set_heater(True)
            self.coordinator.async_set_updated_data(status)
            return
