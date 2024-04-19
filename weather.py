import requests
import datetime
from functools import lru_cache

from config import OPENWEATHER_API_KEY, OPENWEATHER_CITY, OPENWEATHER_COUNTRY

class Weather:

    # 1,000 API calls per day for free
    def __init__(self):
        self.api_key = OPENWEATHER_API_KEY
        self.city_name = OPENWEATHER_CITY
        self.country_code = OPENWEATHER_COUNTRY
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
        self.last_call_date = None

    def is_same_day(self):
        current_date = datetime.date.today()
        return current_date == self.last_call_date

    def get_sunrise_and_sunset(self):
        params = {
            'q': f'{self.city_name},{self.country_code}',
            'appid': self.api_key,
            'units': 'metric',  # Use 'imperial' for Fahrenheit
        }

        response = requests.get(self.base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return int(data['sys']['sunrise']), int(data['sys']['sunset'])
        else:
            print(f"Error: {data['message']}")
            return None

if __name__ == "__main__":

    weather_forecast = Weather()
    sunrise, sunset = weather_forecast.get_sunrise_and_sunset()
    print(f"Sunrise at: {sunrise}, Sunset at: {sunset}")

