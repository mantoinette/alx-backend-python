#!/usr/bin/env python3
"""Test module for utils.py"""
import unittest
from utils import access_nested_map
from utils import memoize



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


if __name__ == '__main__':
    unittest.main()
