# OpenWeatherMap API Wrapper

Simple OpenWeatherMap API Wrapper for Python.

## Installation

```sh
pip install -r requirements.txt
```

If you want to work with CLI, add your API key in `config.py`

```py
API_KEY = "<Your API key>"
```

## Usage

### In your project:

```py
api = WeatherAPI("<Your API key>")
by = api.By

# Find by city name
api.find(by.city("New York"))

# Find by zipcode
api.find(by.zipcode(94040, "us"))

# Find by geo coordinates
api.find(by.coordinates(44.34, 10.99))
```

### From CLI:

```sh
python weather.py city Astana
python weather.py city "New York"

python weather.py zipcode 94040 us

python weather.py coordinates 44.34 10.99
```

![CLI](https://i.imgur.com/yYvuT64.png)
