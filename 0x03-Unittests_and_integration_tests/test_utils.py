#!/usr/bin/env python3
"""Test module for utils.py"""
import unittest
from utils import access_nested_map, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map"""

    def test_access_nested_map(self):
        """Test normal cases"""
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ["a", "b"]), 2)
        self.assertEqual(access_nested_map({"x": {"y": {"z": 5}}}, ["x", "y", "z"]), 5)

    def test_access_nested_map_key_error(self):
        """Test KeyError when path is missing"""
        with self.assertRaises(KeyError):
            access_nested_map({}, ["a"])

        with self.assertRaises(KeyError):
            access_nested_map({"a": 1}, ["a", "b"])


class TestMemoize(unittest.TestCase):
    """Test class for the memoize decorator"""

    def test_memoize(self):
        """Test memoization"""

        class TestClass:
            def __init__(self):
                self.counter = 0

            @memoize
            def method(self):
                self.counter += 1
                return self.counter

        obj = TestClass()

        # First call should increase counter
        result1 = obj.method
        # Second call should return the cached result
        result2 = obj.method

        self.assertEqual(result1, 1)
        self.assertEqual(result2, 1)
        self.assertEqual(obj.counter, 1)  # Confirm method was called only once


if __name__ == '__main__':
    unittest.main()
