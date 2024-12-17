#!/usr/bin/env python3
"""
Client for interacting with the GitHub API.
"""
import requests


class GithubOrgClient:
    """A client to interact with the GitHub API for organization data."""

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Fetch and return organization details."""
        url = f"https://api.github.com/orgs/{self.org_name}"
        response = requests.get(url)
        return response.json()

    def public_repos(self, license=None):
        """Fetch and return a list of public repositories."""
        url = f"https://api.github.com/orgs/{self.org_name}/repos"
        response = requests.get(url)
        repos = response.json()
        if license:
            return [repo["name"] for repo in repos if repo.get("license", {}).get("key") == license]
        return [repo["name"] for repo in repos]


if __name__ == "__main__":
    client = GithubOrgClient("google")
    print(client.org)
    print(client.public_repos())
