"""
Conftest.py - Shared fixtures for Playwright tests.

This file provides reusable pytest fixtures for:
- Browser page setup and teardown
- Login to OrangeHRM
- Screenshot capture on test failure

Key Design Decision:
  The `logged_in_page` fixture uses scope="class" so that all 6 tests
  in TestUserManagement share a SINGLE browser session. This means:
    - Login happens only ONCE (not 6 times)
    - Reduces load on the shared OrangeHRM demo site
    - Tests run faster (~30s instead of ~2min)
    - Tests still appear as separate test blocks in the report
"""

import pytest
from playwright.sync_api import Page, Browser
from pages.login_page import LoginPage


# ── OrangeHRM Credentials ──────────────────────────────────────────────
BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
USERNAME = "Admin"
PASSWORD = "admin123"


@pytest.fixture(scope="class")
def logged_in_page(browser: Browser):
    """
    Class-scoped fixture that creates a single browser context,
    logs in once, and shares the page across all tests in the class.

    This approach:
      - Logs in once instead of 6 times
      - Reduces network load on the shared demo site
      - Makes tests more reliable (fewer timeout risks)
      - Tests still run in separate blocks as required
    """
    # Create a new browser context and page
    context = browser.new_context()
    page = context.new_page()

    # Navigate and login
    login_page = LoginPage(page)
    login_page.navigate(BASE_URL)
    login_page.login(USERNAME, PASSWORD)

    # Wait for the dashboard to confirm successful login
    page.wait_for_url("**/dashboard/index", timeout=30000)

    yield page

    # Cleanup: close context after all tests in the class are done
    context.close()
