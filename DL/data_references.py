"""

References the geographical data for the desired towns

Also references the times in the UNIX format

"""
import time
from geopy.geocoders import Nominatim


def generate_coordinates_city(city):
    """

    Return the latitude and longitude coordinates of a given city

    :param city:
    :return:
    """

    geolocator = Nominatim(user_agent='myapplication', timeout=20)
    location = geolocator.geocode(city)

    return location.latitude, location.longitude


def format_time_horizon(time_horizon):
    """

    Return a formatted unix time for the current time - time_horizon

    :param time_horizon: in days
    :return:
    """

    return int(time.time() - 86400 * time_horizon)


def check_time_horizon(days_horizon):
    """

    Raise an exception if we ask historical data of over 5 days (not supported
    by the free account for OpenWeather)

    :param days_horizon:
    :return:
    """

    if days_horizon > 5:
        raise ValueError('Cannot have historical data of more than 5 days in the past, please change'
                         'the current value of days_horizon, which is set at ' + str(days_horizon))
