#!/usr/bin/env python3
""" Utility functions """

import requests
from typing import Dict, Any, List


def get_json(url: str) -> Dict:
    """Fetches JSON data from a URL"""
    response = requests.get(url)
    return response.json()


def access_nested_map(nested_map: Dict[str, Any], path: List[str]) -> Any:
    """Access a nested dictionary safely.

    Args:
        nested_map (Dict): A dictionary with nested keys.
        path (List[str]): A list of keys representing the path.

    Returns:
        Any: The value at the specified path.

    Raises:
        KeyError: If the key does not exist.
    """
    for key in path:
        if not isinstance(nested_map, dict) or key not in nested_map:
            raise KeyError(f"Key '{key}' not found in nested map")
        nested_map = nested_map[key]
    return nested_map


def memoize(fn):
    """Memoization decorator to cache results."""
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return wrapper
