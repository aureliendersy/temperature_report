"""

Here we access the relevant database and ask for the desired temperature history

"""

import requests
import pandas as pd

from DL.api_key import api_key

api_str_ex = 'https://api.openweathermap.org/data/2.5/onecall?lat=33.441792&lon=-94.037689' \
             '&exclude=minutely&appid={}'.format(api_key)



response = requests.get(api_str_ex)

response_data = response.json()
hourly_data = pd.DataFrame(response_data['hourly'])
daily_data = pd.DataFrame(response_data['daily'])

