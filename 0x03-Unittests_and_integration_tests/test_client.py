#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient  # Adjust the import based on your project structure

class TestGithubOrgClient(unittest.TestCase):
    
    @parameterized.expand([
        ("google", {"org": "google", 
                     "repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"org": "abc", 
                  "repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch('client.GithubOrgClient.get_json')  # Ensure this path is correct
    def test_org(self, org_name, expected_value, mock_get_json):
        # Mock the return value of get_json
        mock_get_json.return_value = expected_value  # Ensure this matches the expected structure
        
        client = GithubOrgClient(org_name)
        result = client.org(org_name)
        
        # Assert that the result matches the expected value
        self.assertEqual(result, expected_value)  # Ensure result is correctly derived
        # Assert that get_json was called once with the expected argument
        mock_get_json.assert_called_once_with(org_name)

        # Additional assertions can be added here if needed
        # For example, check if the length of the result matches expected length
        self.assertEqual(len(result), len(expected_value))  # Check length if necessary

        # Debugging: Print the result and expected value for verification
        print(f"Result: {result}, Expected: {expected_value}")  # Add this line for debugging


    # ... existing code ...

if __name__ == '__main__':
    unittest.main()