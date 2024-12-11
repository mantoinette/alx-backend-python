#!/usr/bin/env python3

"""
This module contains unit tests for the access_nested_map function and utils.get_json.
"""

import unittest
from unittest.mock import patch, Mock
import requests
from utils import access_nested_map, get_json  # Adjust the import based on your project structure

def access_nested_map(nested_map, path):
    """
    Access a nested map using a tuple of keys.

    Args:
        nested_map (dict): The nested map to access.
        path (tuple): A tuple of keys to access the nested map.

    Raises:
        KeyError: If a key in the path is not found in the nested map.
    """
    for key in path:
        if key not in nested_map:
            raise KeyError("Key not found")
        nested_map = nested_map[key]
    return nested_map

class TestAccessNestedMap(unittest.TestCase):
    """
    Test case for the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: any) -> None:
        """
        Test access_nested_map with various inputs.

        Args:
            nested_map (dict): The nested map to test.
            path (tuple): The path to access in the nested map.
            expected (any): The expected result from the access.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test access_nested_map for exceptions.

        Args:
            nested_map (dict): The nested map to test.
            path (tuple): The path to access in the nested map.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), "Key not found")

class TestGetJson(unittest.TestCase):
    """
    Test case for the utils.get_json function.
    """

    @patch('requests.get')
    def test_get_json(self, mock_get):
        # Define test inputs
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for test_url, test_payload in test_cases:
            # Set up the mock to return a response with the desired JSON
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            # Call the get_json function
            result = get_json(test_url)

            # Assert that the mocked get method was called once with the correct URL
            mock_get.assert_called_once_with(test_url)

            # Assert that the result is equal to the expected payload
            self.assertEqual(result, test_payload)

            # Reset the mock for the next iteration
            mock_get.reset_mock()

# To run the tests
if __name__ == "__main__":
    unittest.main()
