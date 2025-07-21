#!/usr/bin/env python3
"""Test module for utils.py"""
import unittest
from parameterized import parameterized
from utils import access_nested_map, memoize


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
        """Test access_nested_map raises KeyError as expected"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_message)


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
