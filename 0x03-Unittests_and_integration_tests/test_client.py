#!/usr/bin/env python3
"""Test module for GithubOrgClient class"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    def test_org(self, org_name):
        """Test that GithubOrgClient.org returns the correct value"""
        with patch('client.get_json') as mock_json:
            test_client = GithubOrgClient(org_name)
            mock_json.return_value = {"name": org_name}
            self.assertEqual(test_client.org(), {"name": org_name})
            mock_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )

    def test_public_repos_url(self):
        """Test that the result of _public_repos_url is the expected one
        based on the mocked payload
        """
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
    def test_public_repos(self, mock_get_json):
        """Test that the list of repos is what you expect from the chosen payload"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = test_payload

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = "hello/world"
            test_client = GithubOrgClient('test')
            result = test_client.public_repos()

            self.assertEqual(result, ['repo1', 'repo2'])
            mock_get_json.assert_called_once_with("hello/world")
            mock_public_repos_url.assert_called_once()


if __name__ == '__main__':
    unittest.main()
