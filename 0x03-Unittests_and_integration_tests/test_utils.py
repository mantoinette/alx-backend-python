#!/usr/bin/env python3

"""
This module contains unit tests for the access_nested_map function.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map  # Adjust the import based on your project structure

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

# To run the tests
if __name__ == "__main__":
    unittest.main()
