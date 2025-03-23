#!/usr/bin/env python3
"""Test module for GithubOrgClient class"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        "google",
        "abc"
    ])
    def test_org(self, org_name):
        """Test that GithubOrgClient.org returns the correct value"""
        test_client = GithubOrgClient(org_name)
        with patch('client.get_json') as mock_get:
            test_client.org()
            mock_get.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )


if __name__ == '__main__':
    unittest.main()
    
