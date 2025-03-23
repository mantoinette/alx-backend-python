#!/usr/bin/env python3
"""Test module for utils.memoize decorator"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Testing GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    def test_org(self, org_name):
        """Test org method"""
        with patch('client.get_json') as mock_json:
            test_client = GithubOrgClient(org_name)
            test_client.org()
            mock_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )

    def test_public_repos_url(self):
        """Test _public_repos_url property"""
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

    @patch('client.get_json')
    def test_public_repos(self, mock_get):
        """Test public_repos method"""
        test_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get.return_value = test_payload

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock,
            return_value="test_url"
        ) as mock_url:
            test_client = GithubOrgClient("test")
            repos = test_client.public_repos()
            
            mock_get.assert_called_once_with("test_url")
            mock_url.assert_called_once()
            self.assertEqual(repos, ["repo1", "repo2"])


if __name__ == '__main__':
    unittest.main()
