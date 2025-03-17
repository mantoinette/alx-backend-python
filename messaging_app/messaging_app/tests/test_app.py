#!/usr/bin/env python3
"""
Test module for the messaging app
"""

def test_sample():
    """Sample test to verify pytest is working"""
    assert True

def test_addition():
    """Test basic addition"""
    assert 1 + 1 == 2

def test_string_operation():
    """Test string operations"""
    assert "hello" + " world" == "hello world"

def test_list_operation():
    """Test list operations"""
    test_list = [1, 2, 3]
    test_list.append(4)
    assert len(test_list) == 4
    assert test_list[-1] == 4 