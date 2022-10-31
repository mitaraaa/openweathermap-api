import requests
from typing import Union

from utils.colors import colored


class Report:
    """
    Python object for OpenWeatherMap API response
    """

    def __init__(self, entries: dict) -> None:
        self.name: str = entries["name"]
        self.country: str = entries["sys"]["country"]
        self.timezone: str = self.__utc(entries["timezone"])
        self.temperature: float = entries["main"]["temp"]
        self.pressure: int = entries["main"]["pressure"]
        self.humidity: int = entries["main"]["humidity"]
        self.wind: int = entries["wind"]["speed"]
        self.visibility: int = entries["visibility"]
        self.weather: dict = entries["weather"]

    def __utc(self, unixtz: int) -> str:
        hours: float = round(unixtz / 3600, 2)
        return "UTC" + f"{hours:+.2f}".zfill(6).replace(".", ":")

    def __emoji(self, weather: str) -> str:
        emojis = {
            "thunderstorm": "⛈️",
            "drizzle": "☔",
            "rain": "🌧️",
            "snow": "🌨️",
            "atmosphere": "🌫️",
            "clear": "☀️",
            "clouds": "☁️",
        }

        return emojis[weather.lower()]

    def __str__(self) -> str:
        emoji_weather = self.__emoji(self.weather[0]["main"])

        return "\n".join(
            (
                f"\n📍 Location: {colored(f'{self.country} - {self.name}')}",
                f"🕒 Timezone: {colored(self.timezone)}\n",
                f"{emoji_weather}  {' / '.join(w['main'] for w in self.weather)}",
                f"🌡️  Temperature:{colored(round(self.temperature), '°C')}",
                f"   Pressure: {colored(self.pressure, ' hPa')}",
                f"💧 Humidity: {colored(f'{self.humidity}%')}",
                f"🍃 Wind: {colored(round(self.wind * 3.6), ' km/h')}\n",
            )
        )


class By:
    """
    URL Generator for OpenWeatherMap API calls

    IMPORTANT: Initialize from WeatherAPI class only!
    """

    BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, key) -> None:
        self.API_KEY = key

    def city(self, city: str) -> str:
        """
        Find by city name
        """
        return f"{self.BASE_URL}?q={city}&appid={self.API_KEY}&units=metric"

    def zipcode(self, zipcode: Union[str, int], country: str) -> str:
        """
        Find by zipcode and country code
        """
        return f"{self.BASE_URL}?zip={zipcode},{country}&appid={self.API_KEY}&units=metric"

    def zipcode(self, location: list) -> str:
        [zipcode, country] = location
        """
        Find by zipcode and country code [zipcode, country]
        """
        return f"{self.BASE_URL}?zip={zipcode},{country}&appid={self.API_KEY}&units=metric"

    def coordinates(
        self, lat: Union[str, float], lon: Union[str, float]
    ) -> str:
        """
        Find by coordinates
        """
        return f"{self.BASE_URL}?lat={lat}&lon={lon}&appid={self.API_KEY}&units=metric"

    def coordinates(self, location: list) -> str:
        [lat, lon] = location
        """
        Find by coordinates [lat, lon]
        """
        return f"{self.BASE_URL}?lat={lat}&lon={lon}&appid={self.API_KEY}&units=metric"


class WeatherAPI:
    """
    Simple OpenWeatherMap API Wrapper for Python.

    Usage:

    ```
    api = WeatherAPI("<Your API key>")
    by = api.By

    # Find by city name
    api.find(by.city("New York"))

    # Find by zipcode
    api.find(by.zipcode(94040, "us"))

    # Find by geo coordinates
    api.find(by.coordinates(44.34, 10.99))
    ```
    """

    def __init__(self, key: str) -> Report:
        self.API_KEY = key
        self.By = By(key)

    def find(self, request_url: str) -> Report:
        """
        Get weather data for given location
        """
        response = requests.get(request_url)

        if response.status_code != 200:
            raise requests.RequestException

        return Report(response.json())
