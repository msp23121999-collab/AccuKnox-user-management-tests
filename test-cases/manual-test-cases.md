# Manual Test Cases — User Management E2E Flow

## Application Under Test

| Field       | Value                                                                               |
|-------------|--------------------------------------------------------------------------------------|
| Application | OrangeHRM Demo                                                                       |
| URL         | https://opensource-demo.orangehrmlive.com/web/index.php/auth/login                    |
| Module      | Admin > User Management > Users                                                      |
| Username    | Admin                                                                                |
| Password    | admin123                                                                             |

---

## Test Cases

### TC_001: Login and Navigate to Admin Module

| Field           | Details                                                                 |
|-----------------|-------------------------------------------------------------------------|
| **Test Scenario**   | Verify user can login and navigate to the Admin module              |
| **Pre-conditions**  | Browser is open. OrangeHRM login page is loaded.                    |
| **Test Steps**      | 1. Enter username: `Admin` <br> 2. Enter password: `admin123` <br> 3. Click the **Login** button <br> 4. Verify Dashboard page is displayed <br> 5. Click **Admin** in the left side menu |
| **Test Data**       | Username: `Admin`, Password: `admin123`                             |
| **Expected Result** | User logs in successfully. Dashboard is displayed. Clicking Admin navigates to the Admin > User Management page. |
| **Actual Result**   | *(to be filled during execution)*                                   |
| **Status**          | *(Pass / Fail)*                                                     |

---

### TC_002: Add a New System User

| Field           | Details                                                                 |
|-----------------|-------------------------------------------------------------------------|
| **Test Scenario**   | Verify a new system user can be added from the Admin module         |
| **Pre-conditions**  | User is logged in as Admin. Admin > User Management page is open.   |
| **Test Steps**      | 1. Click the **+ Add** button <br> 2. Select **User Role**: `ESS` <br> 3. Type employee name hint (e.g., `a`) and select the first suggestion <br> 4. Select **Status**: `Enabled` <br> 5. Enter **Username**: `TestUser_abc12` <br> 6. Enter **Password**: `Test@1234!` <br> 7. Confirm password: `Test@1234!` <br> 8. Click **Save** |
| **Test Data**       | Role: `ESS`, Status: `Enabled`, Username: `TestUser_abc12`, Password: `Test@1234!` |
| **Expected Result** | Success toast message appears: "Successfully Saved". User is redirected to the User list page. |
| **Actual Result**   | *(to be filled during execution)*                                   |
| **Status**          | *(Pass / Fail)*                                                     |

---

### TC_003: Search the Newly Created User

| Field           | Details                                                                 |
|-----------------|-------------------------------------------------------------------------|
| **Test Scenario**   | Verify the newly created user can be found using the search feature  |
| **Pre-conditions**  | User is logged in as Admin. A test user has been created (TC_002).   |
| **Test Steps**      | 1. On the Admin > Users page, enter `TestUser_abc12` in the **Username** search field <br> 2. Click the **Search** button <br> 3. Verify the results table displays at least 1 record <br> 4. Verify the username in the first row matches `TestUser_abc12` |
| **Test Data**       | Search Username: `TestUser_abc12`                                   |
| **Expected Result** | Search results show 1 record. The username, role (`ESS`), and status (`Enabled`) match the created user. |
| **Actual Result**   | *(to be filled during execution)*                                   |
| **Status**          | *(Pass / Fail)*                                                     |

---

### TC_004: Edit User Details (Role, Status, Username)

| Field           | Details                                                                 |
|-----------------|-------------------------------------------------------------------------|
| **Test Scenario**   | Verify all possible user details can be edited                      |
| **Pre-conditions**  | User is logged in as Admin. Test user exists (TC_002).              |
| **Test Steps**      | 1. Search for `TestUser_abc12` <br> 2. Click the **Edit** (pencil) icon on the first result row <br> 3. Change **User Role** from `ESS` to `Admin` <br> 4. Change **Status** from `Enabled` to `Disabled` <br> 5. Change **Username** to `EditedUser_abc12` <br> 6. Click **Save** |
| **Test Data**       | New Role: `Admin`, New Status: `Disabled`, New Username: `EditedUser_abc12` |
| **Expected Result** | Success toast message appears: "Successfully Updated". User is redirected to the Users list page. |
| **Actual Result**   | *(to be filled during execution)*                                   |
| **Status**          | *(Pass / Fail)*                                                     |

---

### TC_005: Validate Updated User Details

| Field           | Details                                                                 |
|-----------------|-------------------------------------------------------------------------|
| **Test Scenario**   | Verify the edited details are saved and displayed correctly         |
| **Pre-conditions**  | User is logged in as Admin. Test user has been edited (TC_004).     |
| **Test Steps**      | 1. Search for `EditedUser_abc12` <br> 2. Verify search returns 1 result <br> 3. Verify username column shows `EditedUser_abc12` <br> 4. Verify user role column shows `Admin` <br> 5. Verify status column shows `Disabled` |
| **Test Data**       | Search Username: `EditedUser_abc12`                                 |
| **Expected Result** | All three fields (Username, User Role, Status) display the updated values correctly. |
| **Actual Result**   | *(to be filled during execution)*                                   |
| **Status**          | *(Pass / Fail)*                                                     |

---

### TC_006: Delete the User

| Field           | Details                                                                 |
|-----------------|-------------------------------------------------------------------------|
| **Test Scenario**   | Verify the user can be deleted from the system                      |
| **Pre-conditions**  | User is logged in as Admin. Edited test user exists (TC_004/TC_005).|
| **Test Steps**      | 1. Search for `EditedUser_abc12` <br> 2. Click the **Delete** (trash) icon on the first result row <br> 3. Confirm deletion by clicking **Yes, Delete** on the confirmation dialog <br> 4. Verify success toast: "Successfully Deleted" <br> 5. Search for `EditedUser_abc12` again <br> 6. Verify "No Records Found" is displayed |
| **Test Data**       | Username to delete: `EditedUser_abc12`                              |
| **Expected Result** | Success toast appears. Searching again returns "No Records Found", confirming the user is deleted. |
| **Actual Result**   | *(to be filled during execution)*                                   |
| **Status**          | *(Pass / Fail)*                                                     |

---

### TC_007: Verify Add User Form Validation (Empty Fields)

| Field           | Details                                                                 |
|-----------------|-------------------------------------------------------------------------|
| **Test Scenario**   | Verify form validation when saving a user with empty required fields|
| **Pre-conditions**  | User is logged in as Admin. Admin > User Management page is open.   |
| **Test Steps**      | 1. Click the **+ Add** button <br> 2. Leave all fields empty <br> 3. Click **Save** <br> 4. Verify validation error messages appear for required fields |
| **Test Data**       | All fields left empty                                               |
| **Expected Result** | Validation error messages appear under each required field: "Required". The form is NOT submitted. |
| **Actual Result**   | *(to be filled during execution)*                                   |
| **Status**          | *(Pass / Fail)*                                                     |

---

### TC_008: Verify Duplicate Username Validation

| Field           | Details                                                                 |
|-----------------|-------------------------------------------------------------------------|
| **Test Scenario**   | Verify the system prevents creating a user with a duplicate username|
| **Pre-conditions**  | User is logged in as Admin. A user with username `Admin` exists.    |
| **Test Steps**      | 1. Click the **+ Add** button <br> 2. Select User Role: `ESS` <br> 3. Enter an employee name <br> 4. Select Status: `Enabled` <br> 5. Enter **Username**: `Admin` (already exists) <br> 6. Enter Password and Confirm Password <br> 7. Observe the validation message |
| **Test Data**       | Username: `Admin` (duplicate)                                       |
| **Expected Result** | Validation error appears: "Already exists". The form does NOT submit.|
| **Actual Result**   | *(to be filled during execution)*                                   |
| **Status**          | *(Pass / Fail)*                                                     |

---

### TC_009: Verify Password Mismatch Validation

| Field           | Details                                                                 |
|-----------------|-------------------------------------------------------------------------|
| **Test Scenario**   | Verify the system shows an error when passwords do not match        |
| **Pre-conditions**  | User is logged in as Admin. Add User form is open.                  |
| **Test Steps**      | 1. Click the **+ Add** button <br> 2. Fill all required fields correctly <br> 3. Enter **Password**: `Test@1234!` <br> 4. Enter **Confirm Password**: `WrongPass!` <br> 5. Click **Save** |
| **Test Data**       | Password: `Test@1234!`, Confirm Password: `WrongPass!`             |
| **Expected Result** | Validation error appears: "Passwords do not match". The form does NOT submit. |
| **Actual Result**   | *(to be filled during execution)*                                   |
| **Status**          | *(Pass / Fail)*                                                     |

---

### TC_010: Verify Reset Button on Search Form

| Field           | Details                                                                 |
|-----------------|-------------------------------------------------------------------------|
| **Test Scenario**   | Verify the Reset button clears all search form fields               |
| **Pre-conditions**  | User is logged in as Admin. Admin > User Management page is open.   |
| **Test Steps**      | 1. Enter a username in the search field <br> 2. Select a User Role filter <br> 3. Click the **Reset** button <br> 4. Verify all search fields are cleared to their default values |
| **Test Data**       | Username: any text, User Role: any selection                        |
| **Expected Result** | All search fields are reset to their default (empty) state. The full user list is displayed again. |
| **Actual Result**   | *(to be filled during execution)*                                   |
| **Status**          | *(Pass / Fail)*                                                     |

---

## Summary

| Test Case | Scenario                           | Priority |
|-----------|------------------------------------|----------|
| TC_001    | Login and Navigate to Admin        | High     |
| TC_002    | Add a New System User              | High     |
| TC_003    | Search the Newly Created User      | High     |
| TC_004    | Edit User Details                  | High     |
| TC_005    | Validate Updated Details           | High     |
| TC_006    | Delete the User                    | High     |
| TC_007    | Form Validation (Empty Fields)     | Medium   |
| TC_008    | Duplicate Username Validation      | Medium   |
| TC_009    | Password Mismatch Validation       | Medium   |
| TC_010    | Reset Button on Search Form        | Low      |
