
""" ARPANSA UV Index"""
import requests
import xml.etree.ElementTree

from homeassistant.const import (
     ATTR_FRIENDLY_NAME, CONF_NAME, CONF_LATITUDE, CONF_LONGITUDE)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle


ARPANSA_DATA_URL = "https://uvdata.arpansa.gov.au/xml/uvvalues.xml"
MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(minutes=1)

""" Map the ARPANSA locations to Lat/Lon from Google maps to find closest station if not explicitly set """
LOCATION_LAT_LON = {
    'Adelaide': [-35.0004451,138.3309764],
    'Alice Springs': [-23.6993534,133.8757526]
}

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([ARPANSASensor()])


class ARPANSASensor(Entity):
    """Representation of an ARPANSA Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Example Temperature'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """UV Index has no unit"""
        return ""

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = 23



def closest_location(lat, lon):
    """Return the closest Location to our lat/lon."""

    def comparable_dist(location):
        """Create a psudeo-distance from latitude/longitude."""
        location_lat = LOCATION_LAT_LON[location][0]
        location_lon = LOCATION_LAT_LON[location][1]
        return (lat - location_lat) ** 2 + (lon - location_lon) ** 2

    return min(LOCATION_LAT_LON, key=comparable_dist)