import json
import requests
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from datetime import timedelta
from datetime import datetime

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from homeassistant.components.sensor import PLATFORM_SCHEMA

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)

CONF_NAME = "name"
CONF_API_KEY = "api_key"
CONF_SN = "sn"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_SN): cv.string
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    solax_cloud = SolaxCloud(
        hass, config[CONF_NAME], config[CONF_API_KEY], config[CONF_SN])
    add_entities([InverterTotalYieldSensor(hass, solax_cloud),
                  InverterDailyYieldSensor(hass, solax_cloud),
                  InverterACPowerSensor(hass, solax_cloud)
                  ], True)


class SolaxCloud:
    def __init__(self, hass, name, api_key, sn):
        self.hass = hass
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key
        self.sn = sn
        self.inverter_name = name
        self.data = {}
        # maybe the user has to change .eu
        self.uri = f'https://www.eu.solaxcloud.com:9443/proxy/api/getRealtimeInfo.do?tokenId={api_key}&sn={sn}'
        self.last_data_time = None

    def get_data(self):
        if not self.data or datetime.now() - self.last_data_time > MIN_TIME_BETWEEN_UPDATES:
            try:
                data = requests.get(self.uri).json()
                if data['success'] == True:
                    self.data = data['result']
                    self.last_data_time = datetime.now()
                    self.logger.info(
                        f'Retrieved new data from solax cloud {self.inverter_name}')
                else:
                    self.data = {}
                    self.logger.error(data['exception'])
            except requests.exceptions.ConnectionError as e:
                self.logger.error(str(e))
                self.data = {}


class InverterTotalYieldSensor(Entity):
    def __init__(self, hass, solax_cloud):
        self._name = solax_cloud.inverter_name + ' Total yield'
        self.hass = hass
        self.solax_cloud = solax_cloud

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        data = self.solax_cloud.data.get('yieldtotal')
        return float('nan') if data is None else data

    @property
    def unit_of_measurement(self):
        return 'kWh'

    @property
    def icon(self):
        return 'mdi:solar-power'

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        self.solax_cloud.get_data()


class InverterDailyYieldSensor(Entity):
    def __init__(self, hass, solax_cloud):
        self._name = solax_cloud.inverter_name + ' Daily yield'
        self.hass = hass
        self.solax_cloud = solax_cloud

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        data = self.solax_cloud.data.get('yieldtoday')
        return float('nan') if data is None else data

    @property
    def unit_of_measurement(self):
        return 'kWh'

    @property
    def icon(self):
        return 'mdi:solar-power'

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        self.solax_cloud.get_data()


class InverterACPowerSensor(Entity):
    def __init__(self, hass, solax_cloud):
        self._name = solax_cloud.inverter_name + ' AC Power'
        self.hass = hass
        self.solax_cloud = solax_cloud

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        data = self.solax_cloud.data.get('acpower')
        return float('nan') if data is None else data

    @property
    def unit_of_measurement(self):
        return 'kW'

    @property
    def icon(self):
        return 'mdi:solar-power'

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        self.solax_cloud.get_data()
