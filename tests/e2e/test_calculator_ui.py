"""End-to-end browser tests for calculator interactions.

Unlike unit or API tests, these tests open the real calculator page in Chromium,
fill its input fields, click its buttons, and check the text shown to the user.
The application server is started once for this module and stopped afterward.
"""

import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import pytest
from playwright.sync_api import Browser, Page, expect, sync_playwright


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def base_url():
    """Start Uvicorn on an available local port and yield the application URL.

    The socket is briefly bound to port zero so the operating system chooses an
    available port. The fixture then waits for the server to respond before
    exposing the URL, and always stops the server when the module tests finish.
    """
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]

    url = f"http://127.0.0.1:{port}"
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=PROJECT_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )

    try:
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            if process.poll() is not None:
                pytest.fail("The Uvicorn server exited before becoming ready.")
            try:
                with urlopen(url, timeout=1):
                    break
            except URLError:
                time.sleep(0.1)
        else:
            pytest.fail("The Uvicorn server did not become ready within 15 seconds.")

        yield url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


@pytest.fixture
def page(base_url: str) -> Page:
    """Launch a fresh Chromium browser page for each UI test."""
    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch()
        try:
            browser_page = browser.new_page()
            browser_page.goto(base_url)
            yield browser_page
        finally:
            browser.close()


@pytest.mark.parametrize(
    # Reuse one interaction test for each operation, button label, and expected
    # result so every calculator button follows the same user-visible flow.
    ("operation", "button", "expected"),
    [
        ("add", "Add", "Calculation Result: 15"),
        ("subtract", "Subtract", "Calculation Result: 5"),
        ("multiply", "Multiply", "Calculation Result: 50"),
        ("divide", "Divide", "Calculation Result: 2"),
    ],
)
def test_calculator_operations(page: Page, operation: str, button: str, expected: str):
    """Submit two numbers through the selected button and verify the result."""
    page.locator("#a").fill("10")
    page.locator("#b").fill("5")

    # Wait for the browser's POST to finish before checking the updated result.
    with page.expect_response(
        lambda response: response.url.endswith(f"/{operation}")
        and response.request.method == "POST"
    ):
        page.get_by_role("button", name=button).click()

    expect(page.locator("#result")).to_have_text(expected)


def test_dividing_by_zero_shows_error(page: Page):
    """Show the API's error message in the page when the divisor is zero."""
    page.locator("#a").fill("10")
    page.locator("#b").fill("0")

    with page.expect_response(
        lambda response: response.url.endswith("/divide")
        and response.request.method == "POST"
    ):
        page.get_by_role("button", name="Divide").click()

    expect(page.locator("#result")).to_have_text(
        "Error: Cannot divide by zero!"
    )
