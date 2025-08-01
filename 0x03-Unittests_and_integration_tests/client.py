import requests
import utils

from utils import get_json


class GithubOrgClient:
    """GitHub Organization Client to interact with GitHub API."""

    def __init__(self, org_name):
        """Initialize with the organization name."""
        self.org_name = org_name

    def org(self):
        """Return the organization data."""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return self.get_json(url)

    def _public_repos_url(self):
        """Return the URL for public repositories."""
        return self.org().get("repos_url")

    def public_repos(self):
        """Return a list of public repositories for the organization."""
        repos_url = self._public_repos_url()
        repos_data = self.get_json(repos_url)
        return [repo["name"] for repo in repos_data]

    def public_repos_with_license(self, license_type):
        """Return a list of public repositories with a specific license."""
        repos = self.public_repos()  # Get the list of repos
        return [repo["name"] for repo in repos if repo["license"]["key"] == license_type]

    def get_json(self, url):
        """Helper method to fetch JSON data from the given URL."""
        response = requests.get(url)
        return response.json()
    repos_data = self.get_json(repos_url)
        return [repo["name"] for repo in repos_data]

    def get_json(self, url):
        """Helper method to fetch JSON data from the given URL."""
        response = requests.get(url)
        return response.json()
