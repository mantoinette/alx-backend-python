#!/usr/bin/env python3
"""
Integration tests for the GithubOrgClient class.
"""
import unittest  # Import the unittest module for creating unit tests
from unittest.mock import patch  # Import patch for mocking objects in tests
from parameterized import parameterized_class  # Import parameterized_class for parameterized tests
from client import GithubOrgClient  # Import the GithubOrgClient class from the client module
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos  # Import fixtures


@parameterized_class([
    {"org_payload": org_payload, "repos_payload": repos_payload, "expected_repos": expected_repos, "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):  # Define the integration test case class

    @classmethod
    def setUpClass(cls):  # Set up the class for integration tests
        cls.get_patcher = patch('requests.get')  # Start patching requests.get
        cls.mock_get = cls.get_patcher.start()  # Start the patcher

        # Mock the responses for the various URLs
        cls.mock_get.side_effect = lambda url: cls.mock_response(url)  # Set side_effect to mock responses

    @classmethod
    def tearDownClass(cls):  # Tear down the class after tests
        cls.get_patcher.stop()  # Stop the patcher

    @classmethod
    def mock_response(cls, url):  # Mock responses based on the URL
        if url == "https://api.github.com/orgs/google":
            return cls.mock_response_with_json(cls.org_payload)
        elif url == "https://api.github.com/orgs/google/repos":
            return cls.mock_response_with_json(cls.repos_payload)
        return cls.mock_response_with_json({})  # Return empty JSON for other URLs

    @staticmethod
    def mock_response_with_json(payload):  # Helper method to create a mock response
        mock_response = patch('requests.Response')  # Create a mock response object
        mock_response.json = lambda: payload  # Mock the json method to return the payload
        return mock_response

    def test_public_repos(self):  # Test the public_repos method
        client = GithubOrgClient("google")  # Create an instance of GithubOrgClient
        repos = client.public_repos()  # Call the public_repos method
        self.assertEqual(repos, self.expected_repos)  # Assert that the returned repos match the expected list


if __name__ == '__main__':  # Check if the script is being run directly
    unittest.main()  # Run the unit tests
