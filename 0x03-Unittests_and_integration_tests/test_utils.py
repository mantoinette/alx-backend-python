#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map  # Assuming this is the correct import

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
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), "Key not found")  # Adjust the message as needed

if __name__ == '__main__':
    unittest.main()
