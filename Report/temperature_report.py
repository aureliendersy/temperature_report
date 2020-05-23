"""

Generate a PDF report for the temperature of the desired cities along the desired timeline

"""

from datetime import date
from DL.temperature_data_download import acquire_all_weather_data
from helpers.reportlab_helper import Document, DataTable, Header, PageBreaker, LineSkip


def main():

    report_date = date.today()
    output_file_name = 'Weather report ' + report_date.strftime('%d-%m-%Y') + '.pdf'
    title_name = 'Weather report ' + report_date.strftime('%d-%m-%Y')

    cities = ['Zurich', 'Cambridge MA']
    full_weather_data = acquire_all_weather_data(cities)

    current_data = full_weather_data['current']
    current_data = current_data[['City', 'temp', 'feels_like', 'humidity', 'pressure', 'uvi', 'wind_speed']]

    report = Document(output_file_name)
    report.add_element(Header(title_name))
    report.add_element(LineSkip(separator=25))
    report.add_element(DataTable(current_data))
    report.build_document()


if __name__ == '__main__':
    main()
