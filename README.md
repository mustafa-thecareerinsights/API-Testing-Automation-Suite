# API Testing Automation Suite

**Project:** API Testing Automation Suite — Software Quality Engineer Assignment  
**Prepared by:** Ruknuddin Asrari  
**Role:** Software Quality Engineer  
**Department:** IT Software Development  
**Organization:** The Career Insights Hub LLC  
**Year:** 2026

---

## Overview

This project is an automated REST API testing suite developed in Python using the Requests library and PyTest. It validates API endpoints for GET, POST, PUT, and DELETE requests and includes both positive and negative test scenarios.

A lightweight sample REST API is included so the reviewer can run the full automation suite locally without needing an external API, database, or credentials.

---

## Deliverables

- Test scripts for REST API automation
- README documentation
- Execution report
- JUnit XML report
- Console execution output
- Positive and negative API test scenarios
- Exception and failure validation

---

## Project Structure

```text
API-Testing-Automation-Suite-Ruknuddin-Asrari/
├── Source code/
│   ├── api_server.py
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── run_tests.bat
│   ├── run_tests.sh
│   └── tests/
│       ├── conftest.py
│       └── test_api_crud.py
├── Execution Report/
│   ├── execution_report.html
│   ├── execution_summary.md
│   ├── junit_results.xml
│   └── pytest_console_output.txt
└── README.md
```

---

## Tested API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Validate API health status |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/<id>` | Retrieve a single task |
| GET | `/tasks?status=open` | Filter tasks by status |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/<id>` | Update an existing task |
| DELETE | `/tasks/<id>` | Delete a task |
| POST | `/reset` | Reset test data before each test |

---

## Test Coverage

| Requirement | Covered |
|---|---|
| Test GET requests | Yes |
| Test POST requests | Yes |
| Test PUT requests | Yes |
| Test DELETE requests | Yes |
| Validate response codes | Yes |
| Validate response payloads | Yes |
| Positive test scenarios | Yes |
| Negative test scenarios | Yes |
| Execution report | Yes |
| API exception/failure handling | Yes |

---

## How to Run

### 1. Open the Source Code folder

```bash
cd "Source code"
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the tests

```bash
python -m pytest -v --junitxml="../Execution Report/junit_results.xml"
```

The PyTest fixture automatically starts the local API server, resets test data before each test, and shuts the server down after execution.

---

## Execution Result

Latest execution result:

```text
13 passed
```

Reports are available in the **Execution Report** folder.

---

## Notes

- The suite uses Python, Requests, and PyTest.
- The sample API uses Python standard library modules for easy local execution.
- Test cases are repeatable because the test data is reset before each test.
- API validations include response status codes, JSON payload fields, error messages, and CRUD behavior.

---

© 2026 Ruknuddin Asrari — Software Quality Engineer — The Career Insights Hub LLC
