#!/usr/bin/env python3
"""Test module for utils.memoize decorator"""
import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Testing memoization"""
    def test_memoize(self):
        """Test that when calling a_property twice, the correct result
        is returned but a_method is only called once using assert_called_once
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_method:
            test_class = TestClass()
            test_class.a_property()
            test_class.a_property()
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
