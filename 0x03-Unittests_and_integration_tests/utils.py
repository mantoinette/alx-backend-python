#!/usr/bin/env python3
""" Utility functions for API requests """

import requests


def get_json(url):
    """Fetches JSON data from a URL"""
    response = requests.get(url)
    return response.json()
