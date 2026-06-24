"""
Test Suite: User Management E2E Flow (Problem Statement 1)

Tests the complete user lifecycle in OrangeHRM Admin module:
  1. Navigate to Admin module
  2. Add a new system user
  3. Search the newly created user
  4. Edit the user details
  5. Validate the updated details
  6. Delete the user

Screenshots are automatically saved to screenshots/ at each key step.
"""

import os
import pytest
import random
import string
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage


# ── Test Data ───────────────────────────────────────────────────────────
RANDOM_SUFFIX = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
TEST_USERNAME = f"TestUser_{RANDOM_SUFFIX}"
EDITED_USERNAME = f"EditedUser_{RANDOM_SUFFIX}"
TEST_PASSWORD = "Test@1234!"
TEST_USER_ROLE = "ESS"
EDITED_USER_ROLE = "Admin"
TEST_STATUS = "Enabled"
EDITED_STATUS = "Disabled"
TEST_EMPLOYEE_NAME_HINT = "a"

# ── Screenshots directory ───────────────────────────────────────────────
SCREENSHOTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "screenshots"
)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def snap(page: Page, name: str):
    """Save a full-page screenshot with a numbered name."""
    path = os.path.join(SCREENSHOTS_DIR, f"{name}.png")
    page.screenshot(path=path, full_page=True)
    print(f"\n  [SCREENSHOT] {name}.png")


class TestUserManagement:
    """
    E2E test class for User Management in OrangeHRM.
    Tests run in order: add -> search -> edit -> validate -> delete.
    """

    # ── TC_001: Navigate to Admin Module ────────────────────────────────

    def test_01_navigate_to_admin_module(self, logged_in_page: Page):
        """
        Test Case 001: Navigate to the Admin module from the Dashboard.

        Steps:
          1. Login is handled by the logged_in_page fixture.
          2. Verify the Dashboard is visible after login.
          3. Navigate to Admin > User Management module.
          4. Verify the Admin page header says 'Admin'.
        """
        # Screenshot 1: Wait for dashboard to fully render then capture
        logged_in_page.wait_for_timeout(2000)
        snap(logged_in_page, "01_login_success_dashboard")

        dashboard = DashboardPage(logged_in_page)
        assert dashboard.is_dashboard_visible(), "Dashboard page did not load after login."

        dashboard.navigate_to_admin()

        # Screenshot 2: Admin page loaded
        snap(logged_in_page, "02_admin_module_loaded")

        admin = AdminPage(logged_in_page)
        assert admin.is_admin_page_visible(), "Admin page did not load successfully."

    # ── TC_002: Add a New User ──────────────────────────────────────────

    def test_02_add_new_user(self, logged_in_page: Page):
        """
        Test Case 002: Add a new system user via the Admin module.

        Steps:
          1. Navigate to Admin module.
          2. Click the '+ Add' button.
          3. Fill in User Role, Employee Name, Status, Username, Password.
          4. Click Save.
          5. Verify success toast message appears.
        """
        dashboard = DashboardPage(logged_in_page)
        dashboard.navigate_to_admin()

        admin = AdminPage(logged_in_page)

        # Click Add — opens form (click_add_button already waits for URL)
        admin.click_add_button()

        # Screenshot 3: Form is loaded, wait briefly for render to settle
        logged_in_page.wait_for_timeout(1000)
        snap(logged_in_page, "03_add_user_form_empty")

        # Fill all fields
        admin.select_user_role(TEST_USER_ROLE)
        admin.enter_employee_name(TEST_EMPLOYEE_NAME_HINT)
        admin.select_status(TEST_STATUS)
        admin.enter_username(TEST_USERNAME)
        admin.enter_password(TEST_PASSWORD)

        # Screenshot 4: Add User form (filled)
        snap(logged_in_page, "04_add_user_form_filled")

        # Save
        admin.click_save()

        # Wait briefly for toast to appear
        logged_in_page.wait_for_timeout(800)

        # Screenshot 5: Success toast
        snap(logged_in_page, "05_add_user_success_toast")

        toast_text = admin.wait_for_success_toast()
        assert "Success" in toast_text, f"Expected success toast but got: {toast_text}"

    # ── TC_003: Search the Newly Created User ───────────────────────────

    def test_03_search_user(self, logged_in_page: Page):
        """
        Test Case 003: Search for the newly created user by username.

        Steps:
          1. Navigate to Admin module.
          2. Enter the test username in the search field.
          3. Click Search.
          4. Verify at least one result appears.
          5. Verify the username in the first row matches.
        """
        dashboard = DashboardPage(logged_in_page)
        dashboard.navigate_to_admin()

        admin = AdminPage(logged_in_page)
        admin.search_user_by_username(TEST_USERNAME)

        # Screenshot 6: Search results
        snap(logged_in_page, "06_search_user_results")

        row_count = admin.get_table_row_count()
        assert row_count >= 1, f"Expected at least 1 result, but found {row_count}."

        row_data = admin.get_first_row_data()
        assert row_data["username"] == TEST_USERNAME, (
            f"Expected '{TEST_USERNAME}' but found '{row_data['username']}'."
        )

    # ── TC_004: Edit User Details ───────────────────────────────────────

    def test_04_edit_user_details(self, logged_in_page: Page):
        """
        Test Case 004: Edit the user's role, status, and username.

        Steps:
          1. Navigate to Admin module.
          2. Search for the test user.
          3. Click the Edit icon on the first row.
          4. Change User Role to 'Admin'.
          5. Change Status to 'Disabled'.
          6. Change Username to the edited username.
          7. Click Save.
          8. Verify success toast.
        """
        dashboard = DashboardPage(logged_in_page)
        dashboard.navigate_to_admin()

        admin = AdminPage(logged_in_page)
        admin.search_user_by_username(TEST_USERNAME)
        admin.click_edit_on_first_row()

        # Screenshot 7: Edit form loaded (click_edit already waits for URL)
        logged_in_page.wait_for_timeout(1000)
        snap(logged_in_page, "07_edit_user_form_opened")

        admin.edit_user_role(EDITED_USER_ROLE)
        admin.edit_status(EDITED_STATUS)
        admin.edit_username(EDITED_USERNAME)

        # Screenshot 8: Edit form filled
        snap(logged_in_page, "08_edit_user_form_filled")

        admin.click_save()

        logged_in_page.wait_for_timeout(800)

        # Screenshot 9: Edit success toast
        snap(logged_in_page, "09_edit_user_success_toast")

        toast_text = admin.wait_for_success_toast()
        assert "Success" in toast_text, f"Expected success toast but got: {toast_text}"

    # ── TC_005: Validate Updated Details ────────────────────────────────

    def test_05_validate_updated_details(self, logged_in_page: Page):
        """
        Test Case 005: Validate that the edited details are correctly saved.

        Steps:
          1. Navigate to Admin module.
          2. Search for the edited username.
          3. Verify the first row shows the updated role, status, and username.
        """
        dashboard = DashboardPage(logged_in_page)
        dashboard.navigate_to_admin()

        admin = AdminPage(logged_in_page)
        admin.search_user_by_username(EDITED_USERNAME)

        # Screenshot 10: Validated updated details in table
        snap(logged_in_page, "10_validate_updated_user_details")

        row_count = admin.get_table_row_count()
        assert row_count >= 1, f"Edited user not found. Got {row_count} results."

        row_data = admin.get_first_row_data()
        assert row_data["username"] == EDITED_USERNAME, (
            f"Username mismatch: expected '{EDITED_USERNAME}', got '{row_data['username']}'."
        )
        assert row_data["user_role"] == EDITED_USER_ROLE, (
            f"Role mismatch: expected '{EDITED_USER_ROLE}', got '{row_data['user_role']}'."
        )
        assert row_data["status"] == EDITED_STATUS, (
            f"Status mismatch: expected '{EDITED_STATUS}', got '{row_data['status']}'."
        )

    # ── TC_006: Delete the User ─────────────────────────────────────────

    def test_06_delete_user(self, logged_in_page: Page):
        """
        Test Case 006: Delete the user and verify they no longer exist.

        Steps:
          1. Navigate to Admin module.
          2. Search for the edited username.
          3. Click the Delete icon on the first row.
          4. Confirm deletion.
          5. Verify success toast.
          6. Search again and verify 'No Records Found'.
        """
        dashboard = DashboardPage(logged_in_page)
        dashboard.navigate_to_admin()

        admin = AdminPage(logged_in_page)
        admin.search_user_by_username(EDITED_USERNAME)

        # Screenshot 11: User found, before deletion
        snap(logged_in_page, "11_before_delete_user")

        admin.delete_first_user_in_table()

        logged_in_page.wait_for_timeout(800)

        # Screenshot 12: Delete success toast
        snap(logged_in_page, "12_delete_user_success_toast")

        toast_text = admin.wait_for_success_toast()
        assert "Success" in toast_text, f"Expected success toast but got: {toast_text}"

        admin.search_user_by_username(EDITED_USERNAME)

        # Screenshot 13: No Records Found after deletion
        snap(logged_in_page, "13_user_deleted_no_records_found")

        assert admin.is_no_records_found(), (
            "User was not deleted — still appears in search results."
        )
