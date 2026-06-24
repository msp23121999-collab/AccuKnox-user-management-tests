"""
LoginPage - Page Object for the OrangeHRM Login Page.

Handles:
- Navigating to the login URL
- Entering username and password
- Clicking the Login button
"""

from playwright.sync_api import Page, expect


class LoginPage:
    """Page Object for OrangeHRM Login Page."""

    # ── Selectors ───────────────────────────────────────────────────────
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button[type='submit']"
    INVALID_CREDENTIALS_MSG = "p.oxd-text--p.oxd-alert-content-text"

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        """Navigate to the login page and wait for it to fully load."""
        self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
        self.page.wait_for_selector(self.USERNAME_INPUT, state="visible", timeout=30000)

    def login(self, username: str, password: str):
        """Fill in credentials and click the Login button."""
        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """Return the text of the invalid credentials error message."""
        error = self.page.locator(self.INVALID_CREDENTIALS_MSG)
        error.wait_for(state="visible", timeout=5000)
        return error.inner_text()
