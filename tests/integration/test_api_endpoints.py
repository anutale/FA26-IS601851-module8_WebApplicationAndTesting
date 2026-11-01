"""Integration tests for the FastAPI application and its HTTP endpoints.

These tests send requests through FastAPI's in-process ``TestClient``. This
exercises routing, request parsing and validation, arithmetic, response
serialization, exception handlers, and request logging together.
"""

import logging

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Provide an HTTP client connected to the application without a live server."""
    return TestClient(app)


def test_get_root_serves_calculator_page(client):
    """The root route should return the calculator's HTML page."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Calculator" in response.text


def test_api_request_is_logged(client, caplog):
    """Successful requests should produce an INFO-level request log."""
    with caplog.at_level(logging.INFO, logger="main"):
        response = client.post("/add", json={"a": 10, "b": 5})

    assert response.status_code == 200
    assert "POST /add completed with status 200" in caplog.text


def test_validation_error_is_logged(client, caplog):
    """Invalid request data should return 400 and produce a warning log."""
    with caplog.at_level(logging.WARNING, logger="main"):
        response = client.post("/add", json={"a": "not-a-number", "b": 5})

    assert response.status_code == 400
    assert "Validation error on /add" in caplog.text


@pytest.mark.parametrize(
    # Each row describes an HTTP request and the JSON result expected from it.
    ("endpoint", "payload", "expected"),
    [
        ("/add", {"a": 10, "b": 5}, {"result": 15.0}),
        ("/subtract", {"a": 10, "b": 5}, {"result": 5.0}),
        ("/multiply", {"a": 10, "b": 5}, {"result": 50.0}),
        ("/divide", {"a": 10, "b": 5}, {"result": 2.0}),
    ],
)
def test_arithmetic_endpoints(client, endpoint, payload, expected):
    """Each arithmetic route should return its calculation in JSON."""
    response = client.post(endpoint, json=payload)

    assert response.status_code == 200
    assert response.json() == expected


def test_divide_by_zero_returns_error(client):
    """Division by zero should be translated to the API's 400 error response."""
    response = client.post("/divide", json={"a": 10, "b": 0})

    assert response.status_code == 400
    assert response.json() == {"error": "Cannot divide by zero!"}


@pytest.mark.parametrize(
    # Include invalid types and missing fields, and identify the field expected
    # in the validation error returned by the application's exception handler.
    ("endpoint", "payload", "expected_error"),
    [
        ("/add", {"a": "ten", "b": 5}, "a"),
        ("/subtract", {"a": 10}, "b"),
        ("/multiply", {"a": 10, "b": "five"}, "b"),
        ("/divide", {"a": 10, "b": "two"}, "b"),
    ],
)
def test_invalid_payload_returns_validation_error(client, endpoint, payload, expected_error):
    """Malformed inputs should return status 400 and identify the bad field."""
    response = client.post(endpoint, json=payload)

    assert response.status_code == 400
    assert "error" in response.json()
    assert expected_error in response.json()["error"]
