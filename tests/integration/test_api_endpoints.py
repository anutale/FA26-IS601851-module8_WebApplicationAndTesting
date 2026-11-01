import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get_root_serves_calculator_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Calculator" in response.text


@pytest.mark.parametrize(
    ("endpoint", "payload", "expected"),
    [
        ("/add", {"a": 10, "b": 5}, {"result": 15.0}),
        ("/subtract", {"a": 10, "b": 5}, {"result": 5.0}),
        ("/multiply", {"a": 10, "b": 5}, {"result": 50.0}),
        ("/divide", {"a": 10, "b": 5}, {"result": 2.0}),
    ],
)
def test_arithmetic_endpoints(client, endpoint, payload, expected):
    response = client.post(endpoint, json=payload)

    assert response.status_code == 200
    assert response.json() == expected


def test_divide_by_zero_returns_error(client):
    response = client.post("/divide", json={"a": 10, "b": 0})

    assert response.status_code == 400
    assert response.json() == {"error": "Cannot divide by zero!"}


@pytest.mark.parametrize(
    ("endpoint", "payload", "expected_error"),
    [
        ("/add", {"a": "ten", "b": 5}, "a"),
        ("/subtract", {"a": 10}, "b"),
        ("/multiply", {"a": 10, "b": "five"}, "b"),
        ("/divide", {"a": 10, "b": "two"}, "b"),
    ],
)
def test_invalid_payload_returns_validation_error(client, endpoint, payload, expected_error):
    response = client.post(endpoint, json=payload)

    assert response.status_code == 400
    assert "error" in response.json()
    assert expected_error in response.json()["error"]
