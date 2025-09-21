#!/usr/bin/env python3
import pytest
from backend import create_app

@pytest.fixture
def client():
    with create_app().test_client() as client:
        yield client