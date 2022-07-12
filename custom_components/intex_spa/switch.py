"""Switch platform for intex_spa."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

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
            IntexSpaSwitch(
                coordinator,
                entry,
                switch="Power",
                icon="mdi:power-plug-outline",
            ),
            IntexSpaSwitch(
                coordinator,
                entry,
                switch="Filter",
                icon="mdi:air-filter",
            ),
            IntexSpaSwitch(
                coordinator,
                entry,
                switch="Jets",
                icon="mdi:weather-windy",
            ),
            IntexSpaSwitch(
                coordinator,
                entry,
                switch="Bubbles",
                icon="mdi:chart-bubble",
            ),
            IntexSpaSwitch(
                coordinator,
                entry,
                switch="Sanitizer",
                icon="mdi:recycle-variant",
            ),
        ]
    )


class IntexSpaSwitch(IntexSpaEntity, SwitchEntity):
    """Intex Spa generic switch class."""

    def __init__(
        self,
        coordinator: IntexSpaDataUpdateCoordinator,
        entry: ConfigEntry,
        icon: str,
        switch: str,
    ):
        super().__init__(coordinator, entry, icon)
        self._switch_type = switch.lower()

        self._attr_name = "{0} {1}".format(
            self.entry.data.get("name", DEFAULT_NAME),
            switch,
        )
        self._attr_unique_id = "{0}_{1}".format(
            self.entry.entry_id,
            self._switch_type,
        )

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        status = await self.coordinator.api.async_set(self._switch_type, True)
        self.coordinator.async_set_updated_data(status)

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        status = await self.coordinator.api.async_set(self._switch_type, False)
        self.coordinator.async_set_updated_data(status)

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return getattr(self.coordinator.data, self._switch_type)
