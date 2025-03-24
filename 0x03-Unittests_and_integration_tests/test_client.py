#!/usr/bin/env python3
"""Test module for GithubOrgClient class"""
import unittest
from unittest.mock import patch, PropertyMock
from utils import get_json, access_nested_map
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import utils  # Ensure utils is properly imported


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    def test_org(self, org_name):
        """Test that GithubOrgClient.org returns the correct value"""
        with patch('utils.get_json') as mock_json:
            test_client = GithubOrgClient(org_name)
            mock_json.return_value = {"name": org_name}
            self.assertEqual(test_client.org(), {"name": org_name})
            mock_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected result"""
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/orgs/google/repos"
            }
            test_client = GithubOrgClient("google")
            self.assertEqual(
                test_client._public_repos_url,
                "https://api.github.com/orgs/google/repos"
            )

    @patch('utils.get_json')
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        mock_get_json.return_value = test_payload

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = "test_url"
            test_client = GithubOrgClient("test")
            result = test_client.public_repos()

            mock_get_json.assert_called_once_with("test_url")
            mock_public_repos_url.assert_called_once()
            self.assertEqual(result, ["repo1", "repo2"])

    @patch('utils.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        """Test public_repos with license filtering"""
        test_payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = test_payload

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = "test_url"
            test_client = GithubOrgClient("test")
            result = test_client.public_repos(license="apache-2.0")

            mock_get_json.assert_called_once_with("test_url")
            mock_public_repos_url.assert_called_once()
            self.assertEqual(result, ["repo1", "repo3"])


if __name__ == '__main__':
    unittest.main()
