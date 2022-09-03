from math import floor
from homeassistant.const import VOLUME_CUBIC_METERS, PERCENTAGE, TEMP_CELSIUS
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from . import sst
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    sst1 = hass.data[DOMAIN][config_entry.entry_id]
    new_devices = []
    # Создать все сенсоры, счетчики, датчики протечки

    for module in sst1.devices:
        if module.get_device_type == 7 or module.get_device_type == 2:
            for counter in module.counters:
                new_devices.append(Counter(counter, module))
            for wSensor in module.wirelessLeakSensors:
                new_devices.append(WirelessLeakSensorBattery(wSensor, module))
        if module.get_device_type == 1:
            new_devices.append(AirTemperature(module))
            new_devices.append(FloorTemperature(module))
        if new_devices:
            async_add_entities(new_devices)


class Counter(Entity):
    _attr_unit_of_measurement = VOLUME_CUBIC_METERS
    # _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_state_class = SensorStateClass.TOTAL

    def __init__(self, counter: sst.Counter, module: sst.LeakModule):
        self._counter = counter
        self._module = module
        # Уникальный идентификатор
        self._attr_unique_id = f"{self._counter.counter_id}_WaterCounter"
        # Отображаемое имя
        self._attr_name = f"WaterCounter {self._counter.counter_name}"
        # Текущее значение
        self._state = self._counter.counter_value / 1000

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._module.get_device_id)}}

    @property
    def icon(self):
        return "mdi:counter"

    @property
    def state(self):
        self._state = self._counter.counter_value / 1000
        return self._state


class WirelessLeakSensorBattery(Entity):
    _attr_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, wirelessLeakSensor, module):
        self._sensor = wirelessLeakSensor
        self._module = module
        # Уникальный идентификатор
        self._attr_unique_id = (
            f"{self._sensor.get_wireless_leak_serial_number}_WireLessLeakSensorBattery"
        )
        # Отображаемое имя
        self._attr_name = f"LeakSensor {self._sensor.get_wireless_leak_sensor_name}"
        # Текущее значение
        self._state = self._sensor.get_wireless_leak_sensor_battery_level

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._module.get_device_id)}}

    @property
    def icon(self):
        return "mdi:battery"

    @property
    def state(self):
        self._state = self._sensor.get_wireless_leak_sensor_battery_level
        return self._state


class AirTemperature(Entity):
    _attr_unit_of_measurement = TEMP_CELSIUS
    # _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, module: sst.ThermostatMCS350):
        self._module = module
        # Уникальный идентификатор
        self._attr_unique_id = f"{self._module._id}_Thermostat_AirTemperature"
        # Отображаемое имя
        self._attr_name = f"ThermostatAirTemperature {self._module._name}"
        # Текущее значение
        self._state = self._module._temperature_air

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._module.get_device_id)}}

    @property
    def icon(self):
        return "mdi:home-thermometer"

    @property
    def state(self):
        self._state = self._module._temperature_air
        return self._state


class FloorTemperature(Entity):
    _attr_unit_of_measurement = TEMP_CELSIUS
    # _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, module: sst.ThermostatMCS350):
        self._module = module
        # Уникальный идентификатор
        self._attr_unique_id = f"{self._module._id}_Thermostat_FloorTemperature"
        # Отображаемое имя
        self._attr_name = f"ThermostatFloorTemperature {self._module._name}"
        # Текущее значение
        self._state = self._module._temperature_floor

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._module.get_device_id)}}

    @property
    def icon(self):
        return "mdi:heating-coil"

    @property
    def state(self):
        self._state = self._module._temperature_floor
        return self._state
