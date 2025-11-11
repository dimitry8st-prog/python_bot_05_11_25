import pytest
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

@pytest.fixture(scope="function")
def event_loop():
    """Event loop для тестов"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()