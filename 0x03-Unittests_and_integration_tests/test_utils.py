#!/usr/bin/env python3

"""
This module contains unit tests for the access_nested_map function.
"""

import unittest
from parameterized import parameterized

def access_nested_map(nested_map, path):
    """
    Access a nested map using a tuple of keys.

    Args:
        nested_map (dict): The nested map to access.
        path (tuple): A tuple of keys to access the nested map.

    Raises:
        KeyError: If a key in the path is not found in the nested map.
    """
    for key in path:
        if key not in nested_map:
            raise KeyError("Key not found")  # Ensure this message matches your test
        nested_map = nested_map[key]
    return nested_map

class TestAccessNestedMap(unittest.TestCase):
    """
    Test case for the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: any) -> None:
        """
        Test access_nested_map with various inputs.

        Args:
            nested_map (dict): The nested map to test.
            path (tuple): The path to access in the nested map.
            expected (any): The expected result from the access.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), "Key not found")  # Ensure this message matches your implementation

# To run the tests
if __name__ == "__main__":
    unittest.main()
