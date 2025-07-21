#!/usr/bin/env python3
"""Test module for utils.py"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, memoize, get_json


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_message):
        """Test access_nested_map raises KeyError with correct message"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_message)


class TestGetJson(unittest.TestCase):
    """Test class for get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test get_json returns correct JSON response from a URL"""
        with patch('utils.requests.get') as mock_get:
            # Mock the response of requests.get().json()
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test class for memoize"""

    def test_memoize(self):
        """Test that memoize caches method output"""
        class TestClass:
            def __init__(self):
                self.counter = 0

            @memoize
            def method(self):
                self.counter += 1
                return self.counter

        obj = TestClass()
        val1 = obj.method
        val2 = obj.method
        self.assertEqual(val1, 1)
        self.assertEqual(val2, 1)
        self.assertEqual(obj.counter, 1)  # should only increment once


if __name__ == '__main__':
    unittest.main()
