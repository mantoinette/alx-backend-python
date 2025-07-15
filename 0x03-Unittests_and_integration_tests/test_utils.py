#!/usr/bin/env python3
"""Test module for utils.py"""
import unittest
from utils import access_nested_map, memoize


class TestAccessNestedMap(unittest.TestCase):
    def test_access_nested_map(self):
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ["a", "b"]), 2)
        self.assertEqual(access_nested_map({"x": {"y": {"z": 5}}}, ["x", "y", "z"]), 5)

    def test_access_nested_map_key_error(self):
        with self.assertRaises(KeyError):
            access_nested_map({}, ["a"])
        with self.assertRaises(KeyError):
            access_nested_map({"a": 1}, ["a", "b"])


class TestMemoize(unittest.TestCase):
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
        self.assertEqual(obj.counter, 1)  # method ran once and result was cached


if __name__ == '__main__':
    unittest.main()
