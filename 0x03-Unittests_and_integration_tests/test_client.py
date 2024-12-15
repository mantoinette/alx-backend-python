#!/usr/bin/env python3
"""
Unit tests for the utils module.
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient  # Adjust the import based on your project structure

class TestGithubOrgClient(unittest.TestCase):
    
    @parameterized.expand([
        ("google", {"org": "google", "repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"org": "abc", "repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch('client.GithubOrgClient.get_json')  # Adjust the path based on your project structure
    def test_org(self, org_name, expected_value, mock_get_json):
        # Mock the return value of get_json
        mock_get_json.return_value = expected_value
        
        client = GithubOrgClient(org_name)
        result = client.org(org_name)
        
        # Assert that the result matches the expected value
        self.assertEqual(result, expected_value)
        # Assert that get_json was called once with the expected argument
        mock_get_json.assert_called_once_with(org_name)

    @patch('client.GithubOrgClient.org')  # Adjust the path based on your project structure
    def test_public_repos_url(self, mock_org):
        # Define a known payload
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
        
        client = GithubOrgClient("google")
        
        # Call the _public_repos_url method
        result = client._public_repos_url
        
        # Assert that the result matches the expected URL
        self.assertEqual(result, "https://api.github.com/orgs/google/repos")

    @patch('client.GithubOrgClient.get_json')  # Mock get_json
    def test_public_repos(self, mock_get_json):
        # Mock the return value of get_json
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        
        # Mock the _public_repos_url property
        with patch('client.GithubOrgClient._public_repos_url', new_callable=property) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/google/repos"
            
            client = GithubOrgClient("google")
            repos = client.public_repos()
            
            # Assert that the list of repos matches the expected output
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            # Assert that get_json was called once
            mock_get_json.assert_called_once()
            # Assert that the mocked property was accessed
            mock_public_repos_url.assert_called_once()

if __name__ == '__main__':
    unittest.main()
