#!/usr/bin/env python3
"""Unit and integration tests for the GithubOrgClient class."""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient

# Sample payloads
org_payload = {"login": "google", "id": 1, "name": "Google"}
repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}},
]
expected_repos = ["repo1", "repo2", "repo3"]
apache2_repos = ["repo1", "repo3"]


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @patch('client.requests.get')
    def test_org(self, mock_get):
        """Test the `org` property."""
        mock_get.return_value.json.return_value = org_payload
        client = GithubOrgClient("google")
        self.assertEqual(client.org, org_payload)
        mock_get.assert_called_once_with("https://api.github.com/orgs/google")

    @patch('client.requests.get')
    def test_public_repos(self, mock_get):
        """Test the `public_repos` method."""
        mock_get.return_value.json.return_value = repos_payload
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, expected_repos)
        mock_get.assert_called_once_with("https://api.github.com/orgs/google/repos")

    @patch('client.requests.get')
    def test_public_repos_with_license(self, mock_get):
        """Test the `public_repos` method with a license filter."""
        mock_get.return_value.json.return_value = repos_payload
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, apache2_repos)
        mock_get.assert_called_once_with("https://api.github.com/orgs/google/repos")


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up the class with mocked responses."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = cls.mock_response

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher."""
        cls.get_patcher.stop()

    @classmethod
    def mock_response(cls, url):
        """Return mocked responses based on the URL."""
        if url == "https://api.github.com/orgs/google":
            return cls.mock_response_with_json(cls.org_payload)
        elif url == "https://api.github.com/orgs/google/repos":
            return cls.mock_response_with_json(cls.repos_payload)
        return cls.mock_response_with_json({})

    @staticmethod
    def mock_response_with_json(payload):
        """Helper method to mock JSON responses."""
        mock_resp = Mock()
        mock_resp.json.return_value = payload
        return mock_resp

    def test_public_repos(self):
        """Test the public_repos method."""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test the public_repos method with a license filter."""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
