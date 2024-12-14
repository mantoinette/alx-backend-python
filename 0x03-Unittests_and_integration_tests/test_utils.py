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

class TestMemoize(unittest.TestCase):
    @patch('utils.TestClass.a_method')  # Mocking a_method
    def test_memoize(self, mock_a_method):
        # Define the TestClass with memoization
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Create an instance of TestClass
        test_instance = TestClass()

        # Call a_property twice
        result_first_call = test_instance.a_property()
        result_second_call = test_instance.a_property()

        # Assertions
        self.assertEqual(result_first_call, 42)  # Check the result
        self.assertEqual(result_second_call, 42)  # Check the result again
        mock_a_method.assert_called_once()  # Ensure a_method was called only once

if __name__ == '__main__':
    unittest.main()
