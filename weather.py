import os
import requests
import sys

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
HELP_MSG = 'weather.py [city | here | -h | --help]\n\t\tcity: city name, either as a single word, or ""\n\t\there: use current location\n\t\t-h --help: show this help\n\n\twhen no arguments are passed to weather.py, the script will prompt the user to input a city\n'


def kelvin_to_celsius(temp):
    return round(temp - 273.15, 2)


def kelvin_to_fahrenheit(temp):
    return round(kelvin_to_celsius(temp) * 9/5 + 32, 2)


def mps_to_mph(speed):
    return round(speed * 2.237, 2)


city = ''

if len(sys.argv) == 1:
    city = input("Enter city name: ").lower()
elif len(sys.argv) == 2:
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print(HELP_MSG)
        sys.exit(0)
    elif sys.argv[1] == 'here':
        get_location = requests.get('http://ipinfo.io')
        city = get_location.json().get('city').lower()
    else:
        city = sys.argv[1].lower()
else:
    print(HELP_MSG)
    sys.exit(1)

request_url = f"{BASE_URL}?appid={API_KEY}&q={city}"

response = requests.get(request_url)

if response.status_code != 200:
    print("Error:", response.status_code)
    sys.exit(1)

data = response.json()
weather = data["weather"]
description = weather[0]["description"]
windspeed = data["wind"]["speed"]
temperature = data["main"]["temp"]
print(city.title())
print(f"Weather\n\t{description.title()}")
print(f"Wind Speed\n\t{mps_to_mph(windspeed)} mph\n\t{windspeed} m/s")
print(
    f"Temperature:\n\t{kelvin_to_fahrenheit(temperature)} F\n\t{kelvin_to_celsius(temperature)} C")
