#!/usr/bin/env python3
"""Test module for utils.py"""
import unittest
from unittest.mock import patch
import utils


class TestUtils(unittest.TestCase):
    """Test class for utils"""

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        """Test get_json function"""
        mock_get.return_value.json.return_value = {"key": "value"}

        result = utils.get_json("http://example.com")
        mock_get.assert_called_once_with("http://example.com")
        self.assertEqual(result, {"key": "value"})


if __name__ == '__main__':
    unittest.main()
