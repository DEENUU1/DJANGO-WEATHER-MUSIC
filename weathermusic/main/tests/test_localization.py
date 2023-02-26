import json
import unittest
from unittest.mock import MagicMock, patch

from main.localization import Geolocation


class TestLocalization(unittest.TestCase):
    """ Test Cases for Localization class methods """
    def setUp(self) -> None:
        with open('main/tests/localization_fixture.json', encoding='utf-8') as json_file:
            self.fake_geolocation_data = json.load(json_file)

    @patch('main.localization.Geolocation._get_ipAddress_information')
    def test_return_localization_success(self, mock_get_information):
        """ Test to successful return the localization """
        mock_get_information.return_value = self.fake_geolocation_data
        self.assertEqual(Geolocation().return_location('192.168.0.1'), 'Lodz')

    @patch('main.localization.Geolocation._get_ipAddress_information')
    def test_return_country_code(self, mock_get_country_code):
        """ Test to successful return the country code """
        mock_get_country_code.return_value = self.fake_geolocation_data
        self.assertEqual(Geolocation().return_country_code('192.168.0.1'), 'PL')

    @patch('main.localization.get')
    def test_get_ipAddress_information(self, get_data):
        """ Test to successful return information from geolocation API """
        json_data = self.fake_geolocation_data
        mock_result = MagicMock()
        mock_result.content = json.dumps(json_data).encode('utf-8')
        get_data.return_value = mock_result
        result = Geolocation()._get_ipAddress_information('192.168.0.1')
        self.assertEqual(result, json_data)
