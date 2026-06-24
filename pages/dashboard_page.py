"""
DashboardPage - Page Object for the OrangeHRM Dashboard.

Handles:
- Verifying successful login by checking the dashboard header
- Navigating to the Admin module via direct URL (most reliable approach)
"""

from playwright.sync_api import Page


ADMIN_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers"


class DashboardPage:
    """Page Object for OrangeHRM Dashboard Page."""

    # ── Selectors ───────────────────────────────────────────────────────
    DASHBOARD_HEADER = "h6.oxd-text.oxd-text--h6.oxd-topbar-header-breadcrumb-module"

    def __init__(self, page: Page):
        self.page = page

    def is_dashboard_visible(self) -> bool:
        """Check if the Dashboard header is visible after login."""
        header = self.page.locator(self.DASHBOARD_HEADER)
        try:
            header.wait_for(state="visible", timeout=15000)
            return "Dashboard" in header.inner_text()
        except Exception:
            return False

    def navigate_to_admin(self):
        """
        Navigate to the Admin > User Management page.

        Uses direct URL navigation (page.goto) instead of clicking the side menu.
        This is the most reliable approach because:
          - Side menu can be slow to render after page transitions
          - Direct URL navigation bypasses any menu animation/loading delays
          - Works consistently whether on Dashboard, Admin, or any other page
        """
        # Only navigate if not already on the Admin Users page
        if "viewSystemUsers" not in self.page.url:
            self.page.goto(ADMIN_URL, wait_until="domcontentloaded", timeout=60000)

        # Wait for the Add button to confirm the page is fully loaded
        self.page.locator("button.oxd-button--secondary").filter(
            has_text="Add"
        ).wait_for(state="visible", timeout=30000)
