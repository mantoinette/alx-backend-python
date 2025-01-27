import unittest
from unittest.mock import patch
from  utils import memoize  # Adjust the import based on your project structure

class TestMemoize(unittest.TestCase):
    """TestMemoize class to test memoization functionality."""

    @patch('test_utils.TestClass.a_method')  # Mocking a_method in TestClass
    def test_memoize(self, mock_a_method):
        """Test that a_property returns the correct value and calls a_method only once."""
        
        class TestClass:
            def a_method(self):
                return 42

            @memoize  # Applying the memoize decorator
            def a_property(self):
                return self.a_method()  # Calls the method to get the value

        test_instance = TestClass()  # Creating an instance of TestClass

        # Call a_property twice
        result_first_call = test_instance.a_property()  # First call to a_property
        result_second_call = test_instance.a_property()  # Second call to a_property

        # Assert the results
        self.assertEqual(result_first_call, 42)  # Assert the first call result
        self.assertEqual(result_second_call, 42)  # Assert the second call result
        mock_a_method.assert_called_once()  # Ensure a_method was called only once

if __name__ == '__main__':
    unittest.main()
