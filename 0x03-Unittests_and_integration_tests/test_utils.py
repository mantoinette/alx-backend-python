"""
test_utils.py

This module contains unit tests for utility functions defined in the utils module.

Tests included:
- TestAccessNestedMap: Tests for the access_nested_map function, including
  cases for valid paths and handling of missing keys.
- TestGetJson: Tests for the get_json function, including mocking HTTP requests
  and verifying the returned JSON payload.
- TestMemoize: Tests for the memoization functionality, ensuring that
  decorated methods are only called once per unique input.

Usage:
    Run this module directly to execute all unit tests.
"""

#!/usr/bin/env python3  # Shebang line to specify the interpreter
import unittest  # Importing the unittest module for testing
from unittest.mock import patch, Mock  # Importing patch and Mock for mocking in tests
from parameterized import parameterized  # Importing parameterized for parameterized tests
from utils import access_nested_map, get_json, memoize  # Importing functions to be tested

class TestAccessNestedMap(unittest.TestCase):  # Test case class for access_nested_map function
    """TestAccessNestedMap class to test access_nested_map function."""
    
    @parameterized.expand([  # Using parameterized to run multiple test cases
        ({"a": 1}, ("a",), 1),  # Test case with a simple dictionary
        ({"a": {"b": 2}}, ("a",), {"b": 2}),  # Test case with nested dictionary
        ({"a": {"b": 2}}, ("a", "b"), 2),  # Test case accessing a nested value
    ])
    def test_access_nested_map(self, nested_map, path, expected):  # Test method for access_nested_map
        self.assertEqual(access_nested_map(nested_map, path), expected)  # Assert the result matches expected

    @parameterized.expand([  # Using parameterized for exception test cases
        ({}, ("a",)),  # Test case with an empty dictionary
        ({"a": 1}, ("a", "b")),  # Test case with a missing key
    ])
    def test_access_nested_map_exception(self, nested_map, path):  # Test method for exceptions
        with self.assertRaises(KeyError):  # Expecting a KeyError
            access_nested_map(nested_map, path)  # Call the function that should raise the exception

class TestGetJson(unittest.TestCase):  # Test case class for get_json function
    """TestGetJson class to test get_json function."""
    
    @parameterized.expand([  # Using parameterized to run multiple test cases
        ("http://example.com", {"payload": True}),  # Test case with a URL and expected payload
        ("http://holberton.io", {"payload": False}),  # Another test case with a different URL
    ])
    @patch('utils.requests.get')  # Mocking the requests.get method
    def test_get_json(self, test_url, test_payload, mock_get):  # Test method for get_json
        mock_response = Mock()  # Creating a mock response object
        mock_response.json.return_value = test_payload  # Setting the return value of json method
        mock_get.return_value = mock_response  # Mocking requests.get to return the mock response

        result = get_json(test_url)  # Call the get_json function with the test URL

        mock_get.assert_called_once_with(test_url)  # Check if requests.get was called with the correct URL
        self.assertEqual(result, test_payload)  # Assert the result matches the expected payload

class TestMemoize(unittest.TestCase):  # Test case class for memoization
    """TestMemoize class to test memoization functionality."""
    
    @patch('utils.TestClass.a_method')  # Mocking a_method in TestClass
    def test_memoize(self, mock_a_method):  # Test method for memoization
        class TestClass:  # Defining a test class for memoization
            def a_method(self):  # Method that returns a constant value
                return 42

            @memoize  # Applying the memoize decorator
            def a_property(self):  # Property method that calls a_method
                return self.a_method()  # Calls the method to get the value

        test_instance = TestClass()  # Creating an instance of TestClass

        result_first_call = test_instance.a_property()  # First call to a_property
        result_second_call = test_instance.a_property()  # Second call to a_property

        self.assertEqual(result_first_call, 42)  # Assert the first call result
        self.assertEqual(result_second_call, 42)  # Assert the second call result
        mock_a_method.assert_called_once()  # Ensure a_method was called only once

if __name__ == '__main__':  # Check if the script is being run directly
    unittest.main()  # Run the unit tests
