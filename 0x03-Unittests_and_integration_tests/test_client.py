#!/usr/bin/env python3
"""Test module for GithubOrgClient class"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.GithubOrgClient.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        test_class = GithubOrgClient(org_name)
        # Configure mock to return a specific value
        mock_get_json.return_value = {"payload": True}
        result = test_class.org()
        # Check if get_json was called with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        # Check if the result matches the mock return value
        self.assertEqual(result, {"payload": True})


if __name__ == '__main__':
    unittest.main()
