"""

Anything that involves putting numbers together

"""


def convert_wind_kmh(dataframe, wind_col_name):
    """

    Convert the wind columns of the dataframe from m/s to km/h

    :param dataframe:
    :param wind_col_name: For reference purposes
    :return:
    """
    new_frame = dataframe.copy()
    new_frame[wind_col_name] = dataframe.copy()[wind_col_name] * 3600 / 1000

    return dataframe
