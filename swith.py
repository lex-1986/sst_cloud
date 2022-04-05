from __future__ import annotations
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from . import sst
from .const import DOMAIN
import logging
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    sst1 = hass.data[DOMAIN][config_entry.entry_id]
    new_devices = []
    for module in sst1.devices:
        new_devices.append(WaterSwitchFirstGroup(module))
        new_devices.append(WaterSwitchSecondGroup(module))
    async_add_entities(new_devices)


class WaterSwitchFirstGroup(SwitchEntity):
    def __init__(self, module: sst.LeakModule):
        self._module = module
        self._attr_unique_id = f"{self._module.get_device_id}_WaterSwitchFirstGroup"
        if self._module.get_first_group_valves_state == "opened":
            self._is_on = True
        else:
            self._is_on = False

    @property
    def name(self):
        return "FirstGroup"

    @property
    def is_on(self):
        if self._module.get_first_group_valves_state == "opened":
            self._is_on = True
        else:
            self._is_on = False
        return self._is_on

    def turn_on(self):
        self._module.open_valve_first_group()
        self._is_on = True

    def turn_off(self):
        self._module.close_valve_first_group()
        self._is_on = False

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._module.get_device_id)}}

    @property
    def icon(self):
        return "mdi:pipe-valve"


class WaterSwitchSecondGroup(SwitchEntity):
    def __init__(self, module: sst.LeakModule):
        self._module = module
        self._attr_unique_id = f"{self._module.get_device_id}_WaterSwitchSecondGroup"
        if self._module.get_second_group_valves_state == "opened":
            self._is_on = True
        else:
            self._is_on = False

    @property
    def name(self):
        return "SecondGroup"

    @property
    def is_on(self):
        if self._module.get_second_group_valves_state == "opened":
            self._is_on = True
        else:
            self._is_on = False
        return self._is_on

    def turn_on(self, **kwargs):
        self._module.open_valve_second_group()

    def turn_off(self, **kwargs):
        self._module.close_valve_second_group()

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._module.get_device_id)}}

    @property
    def icon(self):
        return "mdi:pipe-valve"