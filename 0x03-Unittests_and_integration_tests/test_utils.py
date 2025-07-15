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
        self.assertEqual(access_nested_map(nested_map, path), expected)

    def test_access_nested_map_key_error(self):
        with self.assertRaises(KeyError):
            access_nested_map({}, ("a",))
        with self.assertRaises(KeyError):
            access_nested_map({"a": 1}, ("a", "b"))


class TestMemoize(unittest.TestCase):
    """Test class for memoize"""

    def test_memoize(self):
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
        self.assertEqual(obj.counter, 1)  # should run only once


if __name__ == '__main__':
    unittest.main()
