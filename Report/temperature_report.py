"""

Generate a PDF report for the temperature of the desired cities along the desired timeline

"""

from datetime import date
from DL.temperature_data_download import acquire_all_weather_data
from DL.account_data import target_email_list
from BL.weather_computations import convert_wind_kmh
from BL.email_setup import send_email
from helpers.reportlab_helper import Document, DataTable, Header, PageBreaker, LineSkip, FullPageHeader


def main():

    report_date = date.today()
    report_date_str = report_date.strftime('%d-%m-%Y')
    output_file_name = 'Report_generated/Weather report ' + report_date_str + '.pdf'
    title_name = 'Weather report ' + report_date_str

    cities = ['Zurich', 'Lausanne', 'Cambridge MA']
    full_weather_data = acquire_all_weather_data(cities)

    current_data = full_weather_data['current']
    current_data = current_data[['City', 'temp', 'feels_like', 'humidity', 'pressure', 'uvi', 'wind_speed']]
    current_data = convert_wind_kmh(current_data, 'wind_speed')
    current_data.rename(columns={'temp': 'Temperature (°C)', 'feels_like': 'Apparent Temp (°C)',
                                 'humidity': 'Humidity (%)', 'pressure': 'Pressure (hPa)', 'uvi': 'UV Index',
                                 'wind_speed': 'Wind Speed (km/h)'}, inplace=True)

    report = Document(output_file_name)
    report.add_element(Header(title_name))
    report.add_element(LineSkip(separator=25))
    report.add_element(FullPageHeader('Current weather'))
    report.add_element(LineSkip(separator=10))
    current_weather_table = DataTable(current_data)
    current_weather_table.set_columns_format(['Temperature (°C)', 'Apparent Temp (°C)'], '{:.0f}')
    current_weather_table.set_columns_format(['Wind Speed (km/h)', 'UV Index'], '{:.1f}')
    report.add_element(current_weather_table)
    report.add_element(LineSkip(separator=25))
    report.add_element(FullPageHeader('Forecast to come, stay tuned!'))
    report.build_document()

    for mail_target in target_email_list:
        send_email(mail_target, report_date_str)


if __name__ == '__main__':
    main()
