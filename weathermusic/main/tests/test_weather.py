import json
import unittest
from unittest.mock import MagicMock, patch

from main.weather import Weather


class TestWeather(unittest.TestCase):
    """ Test Cases for Weather Class methods """
    def setUp(self) -> None:
        with open('main/tests/weather_fixture.json', encoding='utf-8') as json_file:
            self.fake_weather_data = json.load(json_file)

    @patch('main.weather.get')
    def test_get_weather_success(self, mock_get):
        """ Test to return weather data from API """
        mock_result = MagicMock()
        mock_result.content = json.dumps(self.fake_weather_data)
        mock_result.status_code = 200
        mock_get.return_value = mock_result
        result = Weather().get_weather('Poland')

        self.assertEqual(result.temp, 1.25)
        self.assertEqual(result.desc, 'overcast clouds')
        self.assertEqual(result.feels_like, -2.83)
        self.assertEqual(result.max_temp, 1.72)
        self.assertEqual(result.min_temp, 0.49)
        self.assertEqual(result.wind_speed, 4.12)