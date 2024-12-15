#!/usr/bin/env python3
"""
Unit tests for the utils module.
"""
import unittest  # Import the unittest module for creating unit tests
from unittest.mock import patch  # Import patch for mocking objects in tests
from parameterized import parameterized  # Import parameterized for parameterized tests
from client import GithubOrgClient  # Import the GithubOrgClient class from the client module


class TestGithubOrgClient(unittest.TestCase):  # Define a test case class

    @parameterized.expand([  # Use parameterized.expand to define multiple test cases
        ("google", {  # First test case for the organization "google"
            "org": "google",  # Expected organization name
            "repos_url": "https://api.github.com/orgs/google/repos"  # Expected repos URL
        }),
        ("abc", {  # Second test case for the organization "abc"
            "org": "abc",  # Expected organization name
            "repos_url": "https://api.github.com/orgs/abc/repos"  # Expected repos URL
        }),
    ])
    @patch('client.GithubOrgClient.get_json')  # Mock the get_json method
    def test_org(self, org_name, expected_value, mock_get_json):  # Define the test method
        # Mock the return value of get_json
        mock_get_json.return_value = expected_value  # Set the mock to return the expected value

        client = GithubOrgClient(org_name)  # Create an instance of GithubOrgClient
        result = client.org(org_name)  # Call the org method

        # Assert that the result matches the expected value
        self.assertEqual(result, expected_value)  # Check if the result is as expected
        # Assert that get_json was called once with the expected argument
        mock_get_json.assert_called_once_with(org_name)  # Verify that get_json was called correctly

    @patch('client.GithubOrgClient.org')  # Mock the org method
    def test_public_repos_url(self, mock_org):  # Define the test method
        # Define a known payload
        mock_org.return_value = {  # Set the mock to return a specific payload
            "repos_url": "https://api.github.com/orgs/google/repos"  # Expected repos URL
        }

        client = GithubOrgClient("google")  # Create an instance of GithubOrgClient

        # Call the _public_repos_url method
        result = client._public_repos_url  # Get the value of the _public_repos_url property

        # Assert that the result matches the expected URL
        self.assertEqual(result, "https://api.github.com/orgs/google/repos")  # Check if the result is as expected

    @patch('client.GithubOrgClient.get_json')  # Mock get_json method
    def test_public_repos(self, mock_get_json):  # Define the test method
        # Mock the return value of get_json
        mock_get_json.return_value = [  # Set the mock to return a list of repositories
            {"name": "repo1"},  # First repository
            {"name": "repo2"},  # Second repository
            {"name": "repo3"},  # Third repository
        ]

        # Mock the _public_repos_url property
        with patch('client.GithubOrgClient._public_repos_url', new_callable=property) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/google/repos"  # Set the mock URL

            client = GithubOrgClient("google")  # Create an instance of GithubOrgClient
            repos = client.public_repos()  # Call the public_repos method

            # Assert that the list of repos matches the expected output
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])  # Check if the returned repos match the expected list
            # Assert that get_json was called once
            mock_get_json.assert_called_once()  # Verify that get_json was called once
            # Assert that the mocked property was accessed
            mock_public_repos_url.assert_called_once()  # Verify that the _public_repos_url property was accessed


if __name__ == '__main__':  # Check if the script is being run directly
    unittest.main()  # Run the unit tests
