"""Shared Playwright fixtures for the portfolio UI test suite."""
import os

import pytest
from playwright.sync_api import sync_playwright

# Site under test. Override with:  BASE_URL=http://localhost:8000 pytest
BASE_URL = os.getenv("BASE_URL", "https://saksham-gif.github.io/")


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Fresh desktop-sized page, opened on the portfolio, for every test."""
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()
    page.goto(BASE_URL, wait_until="domcontentloaded")
    yield page
    context.close()


@pytest.fixture
def mobile_page(browser):
    """Same site at a phone-sized viewport, for responsive-layout checks."""
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    page.goto(BASE_URL, wait_until="domcontentloaded")
    yield page
    context.close()
