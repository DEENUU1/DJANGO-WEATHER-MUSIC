import json
import unittest
from unittest.mock import MagicMock, patch

import responses
from main.spotify import SpotifyCategory, SpotifyAccess


class TestSpotify(unittest.TestCase, SpotifyAccess):
    """ Test Cases for SpotifyCategory and SpotifyAccess class methods """
    @responses.activate
    def test_search_playlist_responses_success(self):
        """ Test success request to the spotify API using responses """
        responses.get(
            url=f"https://api.spotify.com/v1/playlists/6afj5vDI8wGVNrUlRoSsg2",
            json={'external_urls': {'spotify': 'https://testplaylisturl.com'}},
            status=200,
        )

        self.assertEqual(SpotifyCategory._search_playlist(self,'test', '6afj5vDI8wGVNrUlRoSsg2'),
                         'https://testplaylisturl.com')

    @patch('main.spotify.get')
    def test_search_playlist_success(self, mock_get):
        """ Test success request to the spotify API using mock """
        json_data = {'external_urls': {'spotify': 'https://open.spotify.com/playlist/playlist_id'}}
        mock_result = MagicMock()
        mock_result.content = json.dumps(json_data)
        mock_get.return_value = mock_result
        mock_get.return_value.status_code = 200
        result = SpotifyCategory()._search_playlist('123123', 'playlistid123')
        self.assertEqual(result, 'https://open.spotify.com/playlist/playlist_id')

    @patch('main.spotify.get')
    def test_search_playlist_failure(self, mock_get):
        """ Test failed request to the spotify API using mock """
        mock_get.return_value.status_code = 404
        with self.assertRaises(Exception):
            SpotifyCategory()._search_playlist('token', 'playlist_id_123123')

    def test_get_auth_header(self):
        """ Test success get authentication header """
        expected_header = {'Authorization': 'Bearer access_token', 'Content-Type': 'application/json'}
        result_header = SpotifyCategory()._get_auth_header('access_token')
        self.assertEqual(result_header, expected_header)

    @patch('main.spotify.SpotifyCategory.get_random_playlist')
    @patch('main.spotify.get')
    def test_get_random_playlist_success(self, mock_get, mock_playlist):
        """ Test success to return random playlist """
        json_data = {'external_urls': {'spotify': 'https://open.spotify.com/playlist/playlist_id'}}
        mock_result = MagicMock()
        mock_result.content = json.dumps(json_data)
        mock_get.return_value = mock_result
        mock_get.return_value.status_code = 200
        result_search_playlist = SpotifyCategory()._search_playlist('123123', 'playlistid123')

        mock_playlist.return_value = 'https://open.spotify.com/playlist/playlist_id'
        result_random_playlist = SpotifyCategory().get_random_playlist('123123', 'sunny')

        self.assertEqual(result_search_playlist, result_random_playlist)