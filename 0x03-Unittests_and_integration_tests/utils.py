#!/usr/bin/env python3
""" Utility module """

import requests


def get_json(url):
    """GET request to the URL and return the JSON payload"""
    response = requests.get(url)
    return response.json()
