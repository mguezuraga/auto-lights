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
        self.last_sunrise_and_sunset = None

    def is_same_day(self):
        """Check if the current day is the same as the last call date."""
        if not self.last_call_date:
            return False
        return self.last_call_date == datetime.date.today()

    def get_sunrise_and_sunset(self):
        """Fetch new data if the day has changed or return cached data."""
        if self.is_same_day():
            # use cachec data
            return self.last_sunrise_and_sunset

        params = {
            'q': f'{self.city_name},{self.country_code}',
            'appid': self.api_key,
            'units': 'metric',  # Use 'imperial' for Fahrenheit
        }

        response = requests.get(self.base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            self.last_sunrise_and_sunset = int(data['sys']['sunrise']), int(data['sys']['sunset'])
            self.last_call_date = datetime.date.today()
        else:
            print(f"Error: {data['message']}")
            return None
        
        return self.last_sunrise_and_sunset

if __name__ == "__main__":

    weather_forecast = Weather()
    sunrise, sunset = weather_forecast.get_sunrise_and_sunset()
    print(f"Sunrise at: {sunrise}, Sunset at: {sunset}")

