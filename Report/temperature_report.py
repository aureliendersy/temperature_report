"""

Generate a PDF report for the temperature of the desired cities along the desired timeline

"""
from DL.temperature_data_download import acquire_all_weather_data


def main():

    cities = ['Zurich', 'Cambridge MA']
    full_weather_data = acquire_all_weather_data(cities)

    print(full_weather_data)


if __name__ == '__main__':
    main()
