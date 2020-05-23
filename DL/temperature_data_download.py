"""

Here we access the relevant database and ask for the desired temperature history

"""

import requests
import pandas as pd

from DL.account_data import api_key
from DL.data_references import generate_coordinates_city, format_time_horizon, check_time_horizon


def import_current_forecast_data(latitude, longitude):
    """

    Query the historical weather data of a given localization

    Metric is used for the temperature units
    :param latitude
    :param longitude
    :return:
    """

    api_str = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}'.format(latitude, longitude) +\
              '&exclude=minutely&appid={}&units=metric'.format(api_key)

    response = requests.get(api_str)
    response_data = response.json()

    return response_data


def import_historical_data(latitude, longitude, time_horizon):
    """
    
    Query the historical weather data of a given localization 

    Metric is used for the temperature units
    :param latitude
    :param longitude
    :param time_horizon: 
    :return: 
    """

    unix_time = format_time_horizon(time_horizon)
    api_str = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}'.format(latitude) + \
              '&lon={}&dt={}&appid={}&units=metric'.format(longitude, unix_time, api_key)

    response = requests.get(api_str)
    response_data = response.json()

    return response_data


def translate_dict_to_list(data, time_param):
    """

    To create a dataframe we might want to flatten some underlying
    dictionaries (e.g. rain dictionary)

    Valid for current param only

    :param time_param:
    :param data:
    :return:
    """

    if time_param == 'current' and isinstance(data, dict):
        return [data]
    else:
        return data


def format_to_dataframe(response_data, time_parameters, city):
    """

    Return a dictionary of panda frames for each time horizon

    :param response_data:
    :param time_parameters:
    :param city:
    :return:
    """

    dataframes = {}

    for time_param in time_parameters:
        time_reponse = translate_dict_to_list(response_data[time_param], time_param)
        dataframes[time_param] = pd.DataFrame(time_reponse)
        dataframes[time_param]['City'] = city

    return dataframes


def acquire_city_weather_data(city, horizon_days=5):
    """

    For a given city, we acquire all of the required data

    :param city:
    :param horizon_days
    :return:
    """

    # Generate the coordinates
    latitude, longitude = generate_coordinates_city(city)

    # Current Data + Forecast
    data_response_current_forecast = import_current_forecast_data(latitude, longitude)
    full_data = format_to_dataframe(data_response_current_forecast, ['current', 'hourly', 'daily'], city)

    # Historical Data
    historical_snapshot_data = pd.DataFrame()
    historical_hourly_data = pd.DataFrame()

    # Query the required historical data for each time horizon
    for day_horizon in range(1, horizon_days):
        data_response_historical = import_historical_data(latitude, longitude, day_horizon)
        historic_data = format_to_dataframe(data_response_historical, ['current', 'hourly'], city)

        # Add all of the time horizons into one dictionary
        historical_snapshot_data = historical_snapshot_data.append(historic_data['current'], sort=False)
        historical_hourly_data = historical_hourly_data.append(historic_data['hourly'], sort=False)

    # Return a final dictionary with all of the data
    full_data['historical_snapshot'] = historical_snapshot_data
    full_data['historical_hourly'] = historical_hourly_data

    return full_data


def acquire_all_weather_data(cities, horizon_days=5):
    """

    For a list of cities, we acquire all of the weather data and format
    it into one frame

    :param cities:
    :param horizon_days: We can only go up to 5 days
    :return:
    """

    check_time_horizon(horizon_days)
    full_data = {}

    for i, city in enumerate(cities):
        city_data = acquire_city_weather_data(city, horizon_days=horizon_days)

        if i == 0:
            full_data = city_data
        else:
            for time_tags in full_data.keys():
                full_data[time_tags] = full_data[time_tags].append(city_data[time_tags], sort=False)

    return full_data
