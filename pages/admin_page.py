"""
AdminPage - Page Object for the OrangeHRM Admin > User Management Page.

Handles:
- Adding a new system user
- Searching for a user by username
- Editing user details
- Validating user details in the table
- Deleting a user

Selector Strategy:
- Uses LABEL-BASED selectors (Playwright best practice) for form fields.
  Each form field is found by locating the oxd-input-group that contains
  the field's label text, then interacting with the input/dropdown inside.
- This is far more robust than XPath index-based selectors because it
  survives layout changes and doesn't depend on field ordering.
"""

from playwright.sync_api import Page, expect


class AdminPage:
    """Page Object for OrangeHRM Admin (User Management) Page."""

    # ── Selectors ───────────────────────────────────────────────────────

    # Top bar and header
    ADMIN_HEADER = "h6.oxd-text.oxd-text--h6.oxd-topbar-header-breadcrumb-module"

    # Add User button
    ADD_BUTTON = "button.oxd-button.oxd-button--secondary"

    # Save button
    SAVE_BUTTON = "button[type='submit']"

    # Results table
    TABLE_ROWS = "div.oxd-table-body div.oxd-table-card"
    TABLE_CELLS = "div.oxd-table-cell"
    NO_RECORDS_TEXT = "span.oxd-text.oxd-text--span"

    # Delete button and confirmation
    DELETE_BUTTON_IN_ROW = "button i.bi-trash"
    DELETE_CONFIRM_BUTTON = "button.oxd-button.oxd-button--label-danger"

    # Edit button
    EDIT_BUTTON_IN_ROW = "button i.bi-pencil-fill"

    def __init__(self, page: Page):
        self.page = page

    # ── Private Helpers (Label-Based Selectors) ─────────────────────────

    def _get_form_group(self, label_text: str):
        """
        Find the oxd-input-group element that contains a label with the
        given text. This is the core helper for label-based field selection.
        """
        return self.page.locator("div.oxd-input-group").filter(
            has=self.page.locator("label").filter(has_text=label_text)
        )

    def _select_dropdown_by_label(self, label_text: str, option_text: str):
        """
        Find a dropdown by its label text and select an option.

        Steps:
          1. Locate the form group by label
          2. Click the dropdown trigger within it
          3. Wait for the dropdown options list to appear
          4. Click the option matching option_text
        """
        group = self._get_form_group(label_text)
        dropdown_trigger = group.locator("div.oxd-select-text")
        dropdown_trigger.wait_for(state="visible", timeout=5000)
        dropdown_trigger.click()

        # Wait for dropdown options to render
        self.page.wait_for_timeout(500)
        options_container = self.page.locator("div.oxd-select-dropdown")
        options_container.wait_for(state="visible", timeout=5000)

        # Click the matching option
        option = self.page.locator("div.oxd-select-option").filter(
            has_text=option_text
        )
        option.first.wait_for(state="visible", timeout=5000)
        option.first.click()

        # Brief wait for dropdown to close
        self.page.wait_for_timeout(300)

    def _fill_input_by_label(self, label_text: str, value: str):
        """
        Find a text input by its label text and fill it with a value.
        """
        group = self._get_form_group(label_text)
        input_field = group.locator("input.oxd-input")
        input_field.wait_for(state="visible", timeout=5000)
        input_field.fill(value)

    # ── Verification ────────────────────────────────────────────────────

    def is_admin_page_visible(self) -> bool:
        """Verify that the Admin page header is visible."""
        header = self.page.locator(self.ADMIN_HEADER)
        try:
            header.wait_for(state="visible", timeout=10000)
            return "Admin" in header.inner_text()
        except Exception:
            return False

    # ── Add User ────────────────────────────────────────────────────────

    def click_add_button(self):
        """Click the '+ Add' button to open the Add User form."""
        add_btn = self.page.locator(self.ADD_BUTTON).filter(has_text="Add")
        add_btn.wait_for(state="visible", timeout=10000)
        add_btn.click()
        # Wait for the Add User form to load
        self.page.wait_for_url("**/admin/saveSystemUser", timeout=10000)

    def select_user_role(self, role: str):
        """Select a user role from the dropdown (e.g., 'Admin' or 'ESS')."""
        self._select_dropdown_by_label("User Role", role)

    def enter_employee_name(self, name: str):
        """Type an employee name and select the first autocomplete suggestion."""
        group = self._get_form_group("Employee Name")
        emp_input = group.locator("input")
        emp_input.wait_for(state="visible", timeout=10000)
        emp_input.fill("")
        emp_input.type(name, delay=100)

        # Wait for the autocomplete dropdown to appear
        self.page.locator("div.oxd-autocomplete-option").first.wait_for(
            state="visible", timeout=10000
        )

        # CRITICAL: Wait until the "Searching...." placeholder disappears
        # and actual employee names load. Without this, we click "Searching...."
        # which causes an "Invalid" validation error.
        self.page.wait_for_function(
            """
            () => {
                const options = document.querySelectorAll('.oxd-autocomplete-option');
                if (options.length === 0) return false;
                // Check that at least one option does NOT contain "Searching"
                return Array.from(options).some(
                    opt => !opt.textContent.includes('Searching')
                );
            }
            """,
            timeout=15000,
        )

        # Now click the first REAL result
        self.page.locator("div.oxd-autocomplete-option").first.click()

        # Wait for autocomplete to close and value to settle
        self.page.wait_for_timeout(500)

    def select_status(self, status: str):
        """Select status from the dropdown (e.g., 'Enabled' or 'Disabled')."""
        self._select_dropdown_by_label("Status", status)

    def enter_username(self, username: str):
        """Enter the username for the new system user."""
        self._fill_input_by_label("Username", username)

    def enter_password(self, password: str):
        """Enter and confirm the password for the new user."""
        # Password field (exact match to avoid matching 'Confirm Password')
        pwd_group = self.page.locator("div.oxd-input-group").filter(
            has=self.page.locator("label").filter(has_text="Password")
        ).first
        pwd_group.locator("input[type='password']").fill(password)

        # Confirm Password field
        confirm_group = self.page.locator("div.oxd-input-group").filter(
            has=self.page.locator("label").filter(has_text="Confirm Password")
        )
        confirm_group.locator("input[type='password']").fill(password)

    def click_save(self):
        """Click the Save button and wait for the success toast."""
        self.page.locator(self.SAVE_BUTTON).click()

    def add_user(self, role: str, employee_name: str, status: str,
                 username: str, password: str):
        """
        Complete flow to add a new system user.
        Fills all fields and clicks Save.
        """
        self.click_add_button()
        self.select_user_role(role)
        self.enter_employee_name(employee_name)
        self.select_status(status)
        self.enter_username(username)
        self.enter_password(password)
        self.click_save()

    # ── Search User ─────────────────────────────────────────────────────

    def search_user_by_username(self, username: str):
        """Search for a user by typing the username in the search form."""
        self._fill_input_by_label("Username", username)
        self.page.locator(self.SAVE_BUTTON).click()

        # Wait for table to update after search
        self.page.wait_for_timeout(2000)

    def get_table_row_count(self) -> int:
        """Return the number of rows in the results table."""
        self.page.wait_for_timeout(1000)
        rows = self.page.locator(self.TABLE_ROWS)
        return rows.count()

    def get_first_row_data(self) -> dict:
        """
        Extract data from the first row of the results table.
        Returns a dict with keys: username, user_role, employee_name, status.
        """
        first_row = self.page.locator(self.TABLE_ROWS).first
        first_row.wait_for(state="visible", timeout=10000)
        cells = first_row.locator(self.TABLE_CELLS)

        return {
            "username": cells.nth(1).inner_text().strip(),
            "user_role": cells.nth(2).inner_text().strip(),
            "employee_name": cells.nth(3).inner_text().strip(),
            "status": cells.nth(4).inner_text().strip(),
        }

    def is_no_records_found(self) -> bool:
        """Check if 'No Records Found' message is displayed."""
        try:
            no_records = self.page.locator(self.NO_RECORDS_TEXT).filter(
                has_text="No Records Found"
            )
            no_records.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    # ── Edit User ───────────────────────────────────────────────────────

    def click_edit_on_first_row(self):
        """Click the edit (pencil) icon on the first row of the results table."""
        edit_btn = self.page.locator(self.TABLE_ROWS).first.locator(
            self.EDIT_BUTTON_IN_ROW
        )
        edit_btn.wait_for(state="visible", timeout=10000)
        edit_btn.click()

        # Wait for the edit form to load
        self.page.wait_for_url("**/admin/saveSystemUser/**", timeout=10000)

    def edit_user_role(self, new_role: str):
        """Change the user role on the edit form."""
        self.select_user_role(new_role)

    def edit_status(self, new_status: str):
        """Change the status on the edit form."""
        self.select_status(new_status)

    def edit_username(self, new_username: str):
        """Change the username on the edit form."""
        self._fill_input_by_label("Username", new_username)

    # ── Delete User ─────────────────────────────────────────────────────

    def click_delete_on_first_row(self):
        """Click the delete (trash) icon on the first row of the results table."""
        delete_btn = self.page.locator(self.TABLE_ROWS).first.locator(
            self.DELETE_BUTTON_IN_ROW
        )
        delete_btn.wait_for(state="visible", timeout=10000)
        delete_btn.click()

    def confirm_delete(self):
        """Click 'Yes, Delete' on the confirmation dialog."""
        confirm_btn = self.page.locator(self.DELETE_CONFIRM_BUTTON)
        confirm_btn.wait_for(state="visible", timeout=5000)
        confirm_btn.click()

    def delete_first_user_in_table(self):
        """Complete flow to delete the first user in the results table."""
        self.click_delete_on_first_row()
        self.confirm_delete()

    # ── Toast / Success Messages ────────────────────────────────────────

    def wait_for_success_toast(self) -> str:
        """Wait for and return the success toast message text."""
        toast = self.page.locator("div.oxd-toast--success")
        toast.wait_for(state="visible", timeout=10000)
        text = toast.inner_text()
        # Wait for toast to disappear before continuing
        toast.wait_for(state="hidden", timeout=10000)
        return text
