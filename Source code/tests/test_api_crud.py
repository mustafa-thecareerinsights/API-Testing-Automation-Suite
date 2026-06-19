"""
Automated REST API tests using Requests and PyTest.
Prepared by: Ruknuddin Asrari
"""

import requests

BASE_URL = "http://127.0.0.1:5060"


def test_health_check_returns_200():
    response = requests.get(f"{BASE_URL}/health", timeout=3)

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["status"] == "healthy"


def test_get_all_tasks_returns_expected_payload():
    response = requests.get(f"{BASE_URL}/tasks", timeout=3)

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["count"] == 2
    assert isinstance(body["data"], list)
    assert {"id", "title", "status", "priority"}.issubset(body["data"][0].keys())


def test_get_single_task_positive_scenario():
    response = requests.get(f"{BASE_URL}/tasks/1", timeout=3)

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["id"] == 1
    assert body["data"]["title"] == "Validate login API"


def test_get_single_task_negative_not_found():
    response = requests.get(f"{BASE_URL}/tasks/999", timeout=3)

    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["error"] == "Task not found"


def test_post_create_task_positive_scenario():
    payload = {
        "title": "Validate payment API",
        "status": "open",
        "priority": "critical",
    }

    response = requests.post(f"{BASE_URL}/tasks", json=payload, timeout=3)

    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["id"] == 3
    assert body["data"]["title"] == payload["title"]
    assert body["data"]["priority"] == "critical"


def test_post_create_task_negative_missing_title():
    payload = {"status": "open", "priority": "high"}

    response = requests.post(f"{BASE_URL}/tasks", json=payload, timeout=3)

    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["error"] == "title is required"


def test_post_create_task_negative_invalid_status():
    payload = {"title": "Invalid status test", "status": "blocked", "priority": "high"}

    response = requests.post(f"{BASE_URL}/tasks", json=payload, timeout=3)

    assert response.status_code == 400
    assert response.json()["error"] == "invalid status"


def test_put_update_task_positive_scenario():
    payload = {"status": "resolved", "priority": "medium"}

    response = requests.put(f"{BASE_URL}/tasks/1", json=payload, timeout=3)

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "resolved"
    assert body["data"]["priority"] == "medium"


def test_put_update_task_negative_not_found():
    payload = {"status": "closed"}

    response = requests.put(f"{BASE_URL}/tasks/999", json=payload, timeout=3)

    assert response.status_code == 404
    assert response.json()["error"] == "Task not found"


def test_put_update_task_negative_invalid_priority():
    payload = {"priority": "urgent"}

    response = requests.put(f"{BASE_URL}/tasks/1", json=payload, timeout=3)

    assert response.status_code == 400
    assert response.json()["error"] == "invalid priority"


def test_delete_task_positive_scenario():
    response = requests.delete(f"{BASE_URL}/tasks/2", timeout=3)

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["deleted_id"] == 2

    verify_response = requests.get(f"{BASE_URL}/tasks/2", timeout=3)
    assert verify_response.status_code == 404


def test_delete_task_negative_not_found():
    response = requests.delete(f"{BASE_URL}/tasks/999", timeout=3)

    assert response.status_code == 404
    assert response.json()["error"] == "Task not found"


def test_filter_tasks_by_status():
    response = requests.get(f"{BASE_URL}/tasks?status=open", timeout=3)

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["count"] == 1
    assert body["data"][0]["status"] == "open"
