from requests import get
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('GEOLOCATION_KEY')


def get_ip(request):
    ip_address = request.META.get('HTTP_X_FORWARDER_FOR')
    if ip_address:
        ip = ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip