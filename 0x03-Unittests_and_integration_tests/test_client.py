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

if __name__ == '__main__':
    unittest.main()

