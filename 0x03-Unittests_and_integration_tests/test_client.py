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
    def test_org(self, org_name):
        """Test that GithubOrgClient.org returns the correct value"""
        with patch('client.get_json') as mock_json:
            mock_json.return_value = {"login": org_name}
            test_class = GithubOrgClient(org_name)
            self.assertEqual(test_class.org(), {"login": org_name})
            mock_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )


if __name__ == '__main__':
    unittest.main()
