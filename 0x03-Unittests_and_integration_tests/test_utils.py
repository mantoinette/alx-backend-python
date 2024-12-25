#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize  # Assuming this is the correct import

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),  # Test case 1
        ({"a": 1}, ("a", "b")),  # Test case 2
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)

class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')  # Mocking requests.get
    def test_get_json(self, test_url, test_payload, mock_get):
        # Create a mock response object with a json method
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the get_json function
        result = get_json(test_url)

        # Assertions
        mock_get.assert_called_once_with(test_url)  # Check if requests.get was called with the correct URL
        self.assertEqual(result, test_payload)  # Check if the result matches the expected payload

class TestUtils(unittest.TestCase):
    
    def test_example(self):
        # Example of breaking long lines
        some_long_variable_name = (
            "This is a very long string that exceeds the character limit"
        )  # E501
        self.assertEqual(len(some_long_variable_name), 78)  # Example assertion

    def test_another_example(self):
        another_long_variable_name = (
            "Another long string that also exceeds the character limit"
        )  # E501
        self.assertTrue("long" in another_long_variable_name)

# ... existing code ...

if __name__ == '__main__':
    unittest.main()