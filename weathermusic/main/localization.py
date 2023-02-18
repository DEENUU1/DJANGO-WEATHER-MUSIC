import json
import os

from dotenv import load_dotenv
from requests import get

load_dotenv()

""" Returning geolocation information from IP address"""


class IPScraper:

    def get_ipaddress(self, request) -> str:
        """ Method that is getting user's ip address"""

        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            ip = ip_address.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip


class Geolocation:
    """ This class allows to get user localization based on the user's ip address """

    def __init__(self):
        self.api_key = os.getenv('GEOLOCATION_KEY')

    def _get_ipAddress_information(self, ip_address: str) -> json:
        """ Method that is returning data based on the IP """

        base_url = f'https://ipgeolocation.abstractapi.com/v1/?api_key={self.api_key}'
        result = get(base_url)
        json_result = json.loads(result.content)
        return json_result

    def _get_key_by_value(self, key: str, ip_address: str) -> str:
        json_result = self._get_ipAddress_information(ip_address)
        return json_result.get(key)

    def return_location(self, ip_address: str) -> str:
        """ Method that is returning city name based on the IP """
        return self._get_key_by_value('city', ip_address)

    def return_country_code(self, ip_address: str) -> str:
        """ Method that is returning country code based on the IP """
        return self._get_key_by_value('country_code', ip_address)