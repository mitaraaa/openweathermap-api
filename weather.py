import argparse
from api import WeatherAPI

import config


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        "weather.py",
        description="Get weather info for given location",
        usage=f"\npython weather.py city <location>\n{' ' * 18}zipcode <zip> <country>\n{' ' * 18}coordinates <lat> <lon>",
    )

    subparsers = parser.add_subparsers(dest="type")

    city_parser = subparsers.add_parser("city", help="Search by city")
    city_parser.add_argument("location", help="City name")

    zip_parser = subparsers.add_parser("zipcode", help="Search by ZIP code")
    zip_parser.add_argument("location", help="Zip code, country code", nargs=2)

    geo_parser = subparsers.add_parser(
        "coordinates", help="Search by coordinates"
    )
    geo_parser.add_argument("location", help="Latitude, longitude", nargs=2)

    return parser


def find(t: str, location):
    api = WeatherAPI(config.API_KEY)
    by = api.By

    print(api.find(getattr(by, t)(location)))


if __name__ == "__main__":
    parser = parser()
    args = parser.parse_args()
    find(args.type, args.location)
