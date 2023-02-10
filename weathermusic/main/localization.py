from requests import get
from dotenv import load_dotenv
import os
import json

load_dotenv()


class Geolocation:
    """ This class allows to get user localization based on the user's ip address """

    def __init__(self):
        self.api_key = os.getenv('GEOLOCATION_KEY')

    @staticmethod
    def get_ipaddress(request) -> str:
        """ Method that is getting user's ip address"""

        ip_address = request.META.get('HTTP_X_FORWARDER_FOR')
        if ip_address:
            ip = ip_address.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip

    def return_location(self, ip_address: str) -> str:
        """ Method that is returning city name based on the IP """

        base_url = f'https://ipgeolocation.abstractapi.com/v1/?api_key={self.api_key}'
        result = get(base_url)
        json_result = json.loads(result.content)

        if result.status_code == 200:
            city_name = json_result["city"]
            return city_name
        else:
            raise Exception('Nie działa')
