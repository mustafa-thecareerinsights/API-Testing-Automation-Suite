"""PyTest fixtures for API Testing Automation Suite."""

import os
import subprocess
import sys
import time

import pytest
import requests

BASE_URL = "http://127.0.0.1:5060"


@pytest.fixture(scope="session", autouse=True)
def api_server():
    """Start the local sample API before tests and stop it after tests."""
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    server_file = os.path.join(project_dir, "api_server.py")

    process = subprocess.Popen(
        [sys.executable, server_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    for _ in range(30):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=1)
            if response.status_code == 200:
                break
        except requests.RequestException:
            time.sleep(0.25)
    else:
        process.terminate()
        raise RuntimeError("API server did not start within the expected time.")

    yield

    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


@pytest.fixture(autouse=True)
def reset_test_data():
    """Reset API data before every test for stable and repeatable execution."""
    requests.post(f"{BASE_URL}/reset", timeout=3)
    yield
