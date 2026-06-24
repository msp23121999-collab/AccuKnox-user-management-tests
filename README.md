# AccuKnox QA Trainee — User Management Test Automation

> **A complete end-to-end test automation project for the OrangeHRM User Management module.**
> Built with Python, Playwright, and pytest as part of the AccuKnox QA Trainee Practical Assessment.

---

## 📌 What Is This Project?

This project automates testing of the **OrangeHRM** web application — specifically the **Admin > User Management** module.

It was built for the **AccuKnox QA Trainee Practical Assessment** and covers two problem statements:

| Problem Statement | What It Does |
|---|---|
| **PS1 — User Management E2E** | Automatically logs in, adds a user, searches them, edits their details, validates the changes, and finally deletes them — all in one automated flow |
| **PS2 — System & App Health** | Two Python scripts that check your computer's health (CPU, RAM, Disk) and check if websites are online or offline |

---

## 🌐 Application Under Test

| Detail | Value |
|---|---|
| **Application** | OrangeHRM (Open Source HR Software) |
| **URL** | https://opensource-demo.orangehrmlive.com/web/index.php/auth/login |
| **Login Username** | `Admin` |
| **Login Password** | `admin123` |
| **Module Tested** | Admin → User Management → System Users |

---

## 📂 Project Folder Structure

Here is what every file and folder does:

```
AccuKnox-user-management-tests/
│
├── 📁 pages/                          ← Page Object Model (POM) classes
│   ├── login_page.py                  ← Handles login form (enter username, password, click Login)
│   ├── dashboard_page.py              ← Handles navigation to the Admin module
│   └── admin_page.py                  ← Handles all user management actions (add/search/edit/delete)
│
├── 📁 tests/
│   └── test_user_management.py        ← The 6 automated test cases (the main test file)
│
├── 📁 test-cases/
│   ├── manual-test-cases.md           ← 10 manual test cases written in plain text (Markdown)
│   └── User_Management_Test_Cases.xlsx← Same 10 test cases in Excel format for submission
│
├── 📁 problem-statement-2/
│   ├── system_health_monitor.py       ← Checks CPU, Memory, Disk usage of your computer
│   └── app_health_checker.py          ← Checks if websites/apps are UP or DOWN
│
├── 📁 screenshots/                    ← Auto-captured screenshots from test runs (evidence)
├── 📁 reports/                        ← HTML test report generated after each run
├── 📁 logs/                           ← Log files from the PS2 scripts
│
├── 📁 .github/workflows/
│   └── playwright-tests.yml           ← GitHub Actions — runs tests automatically on every push
│
├── conftest.py                        ← Shared test setup (login session shared across all tests)
├── pytest.ini                         ← Pytest settings (browser, base URL, timeout)
├── requirements.txt                   ← All Python packages needed (install with pip)
├── .gitignore                         ← Tells Git which files NOT to upload (venv, logs, etc.)
└── README.md                          ← This file — project documentation
```

---

## 🛠️ Technologies Used

| Tool / Library | What It's Used For |
|---|---|
| **Python 3.11** | The programming language everything is written in |
| **Playwright** | Controls the browser — clicks buttons, fills forms, reads text |
| **pytest** | Runs the tests and collects results |
| **pytest-playwright** | Connects Playwright with pytest |
| **pytest-html** | Generates a nice HTML report after tests run |
| **psutil** | Reads CPU, memory, disk info from the OS (PS2) |
| **requests** | Sends HTTP requests to check if websites are up (PS2) |
| **openpyxl** | Used to generate the Excel test case document |
| **GitHub Actions** | Automatically runs tests every time code is pushed to GitHub |

---

## ✅ Prerequisites — What You Need Before Starting

Before setting up this project, make sure you have these installed on your computer:

### 1. Python 3.11 or higher
- Download from: https://www.python.org/downloads/
- ⚠️ **Important:** During installation, check the box **"Add Python to PATH"**
- Verify it works: open PowerShell and type `python --version`

### 2. Git
- Download from: https://git-scm.com/downloads
- Verify it works: open PowerShell and type `git --version`

### 3. A Code Editor (optional but recommended)
- Download **VS Code** from: https://code.visualstudio.com/

---

## 🚀 Setup Guide — Step by Step

Follow these steps exactly to get the project running on your computer.

---

### Step 1 — Clone the Repository

Open **PowerShell** and run:

```powershell
git clone https://github.com/YOUR_USERNAME/AccuKnox-user-management-tests.git
cd AccuKnox-user-management-tests
```

> **What this does:** Downloads the project from GitHub to your computer.

---

### Step 2 — Create a Virtual Environment

```powershell
python -m venv venv
```

> **What this does:** Creates an isolated Python environment just for this project.
> This means packages installed here won't affect other Python projects.

---

### Step 3 — Activate the Virtual Environment

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**On Windows (CMD):**
```cmd
.\venv\Scripts\activate.bat
```

**On Linux / macOS:**
```bash
source venv/bin/activate
```

> **How to know it worked:** You'll see `(venv)` appear at the start of your terminal line.

---

### Step 4 — Install All Dependencies

```powershell
pip install -r requirements.txt
```

> **What this does:** Installs all required Python libraries listed in `requirements.txt`
> (Playwright, pytest, psutil, requests, etc.)

---

### Step 5 — Install the Playwright Browser

```powershell
python -m playwright install chromium
```

> **What this does:** Downloads the Chromium browser that Playwright uses to automate testing.
> This is separate from your regular Chrome browser.

---

### Step 6 — Verify Everything Is Installed

```powershell
python -m playwright --version
pytest --version
```

> You should see version numbers printed. If you do — you are ready to run the tests!

---

## 🧪 Running Problem Statement 1 — Automated Tests

### Run All 6 Tests (Headless — No Browser Window)

```powershell
pytest tests/test_user_management.py -v --html=reports/test-report.html --self-contained-html
```

### Run All 6 Tests (Headed — Watch the Browser in Action)

```powershell
pytest tests/test_user_management.py -v --headed --slowmo=1000 --html=reports/test-report.html --self-contained-html
```

> **`--headed`** = opens a real browser window so you can watch every action  
> **`--slowmo=1000`** = slows each step by 1 second so it's easy to follow

### Expected Output

```
tests/test_user_management.py::TestUserManagement::test_01_navigate_to_admin_module[chromium] PASSED
tests/test_user_management.py::TestUserManagement::test_02_add_new_user[chromium]             PASSED
tests/test_user_management.py::TestUserManagement::test_03_search_user[chromium]              PASSED
tests/test_user_management.py::TestUserManagement::test_04_edit_user_details[chromium]        PASSED
tests/test_user_management.py::TestUserManagement::test_05_validate_updated_details[chromium] PASSED
tests/test_user_management.py::TestUserManagement::test_06_delete_user[chromium]              PASSED

======================== 6 passed in ~60s ========================
```

### View the HTML Report

After running, open this file in your browser:
```
reports/test-report.html
```
It shows pass/fail status, execution time, and error details for every test.

---

## 📋 What Each Test Does

| Test | What It Automates |
|---|---|
| **test_01** — Navigate to Admin | Logs in with Admin credentials → verifies Dashboard loads → navigates to Admin > User Management |
| **test_02** — Add New User | Clicks "+ Add" → fills User Role, Employee Name, Status, Username, Password → clicks Save → verifies success toast |
| **test_03** — Search User | Enters the username in the search box → clicks Search → verifies the user appears in results |
| **test_04** — Edit User | Clicks the Edit (pencil) icon → changes User Role to Admin, Status to Disabled, Username → saves |
| **test_05** — Validate Changes | Searches the edited username → verifies all 3 updated fields (Role, Status, Username) are correct |
| **test_06** — Delete User | Clicks the Delete (trash) icon → confirms deletion → searches again → verifies "No Records Found" |

---

## 📸 Screenshots — Evidence of Test Execution

The tests automatically save screenshots at every key step.

After running the tests, check the `screenshots/` folder:

| Screenshot File | What It Shows |
|---|---|
| `00_login_page.png` | The OrangeHRM login page |
| `01_login_success_dashboard.png` | Dashboard after successful login |
| `02_admin_module_loaded.png` | Admin > User Management page |
| `03_add_user_form_empty.png` | The empty Add User form |
| `04_add_user_form_filled.png` | Add User form with all fields filled |
| `05_add_user_success_toast.png` | Green success toast after adding user |
| `06_search_user_results.png` | Search results showing the new user |
| `07_edit_user_form_opened.png` | Edit User form opened |
| `08_edit_user_form_filled.png` | Edit form with changed values |
| `09_edit_user_success_toast.png` | Success toast after editing |
| `10_validate_updated_user_details.png` | Updated details confirmed in the table |
| `11_before_delete_user.png` | User in table, ready to be deleted |
| `12_delete_user_success_toast.png` | Success toast after deletion |
| `13_user_deleted_no_records_found.png` | "No Records Found" — user fully deleted |
| `ps2_01_system_health_monitor.png` | System health script output |
| `ps2_02_app_health_checker.png` | App health checker output |

---

## 🏗️ How the Code Is Organised (Page Object Model)

This project uses the **Page Object Model (POM)** design pattern.

**The idea is simple:**
- Think of each page of the website as a separate class in Python.
- Each class has methods (functions) that represent actions on that page.
- Tests just call those methods — they don't directly click buttons or fill forms.

**Example:**
```
Instead of writing this in every test:
  page.fill("input[name='username']", "Admin")
  page.click("button[type='submit']")

We write this:
  login_page.login("Admin", "admin123")
```

This makes the code much cleaner, easier to read, and easier to maintain.

### The 3 Page Objects:

**`login_page.py`** — Controls the Login Page
- `navigate(url)` → Opens the login page
- `login(username, password)` → Fills credentials and clicks Login

**`dashboard_page.py`** — Controls the Dashboard
- `is_dashboard_visible()` → Checks if login was successful
- `navigate_to_admin()` → Goes to the Admin > User Management page

**`admin_page.py`** — Controls the Admin User Management Page
- `add_user(role, employee, status, username, password)` → Adds a new user
- `search_user_by_username(username)` → Searches for a user
- `click_edit_on_first_row()` → Clicks the Edit button
- `edit_user_role(role)` → Changes the User Role
- `edit_status(status)` → Changes the Status
- `edit_username(username)` → Changes the Username
- `delete_first_user_in_table()` → Deletes the user and confirms
- `wait_for_success_toast()` → Waits for and returns the success message
- `is_no_records_found()` → Checks if the table shows "No Records Found"

---

## 📝 Manual Test Cases

The manual test cases are available in two formats:

| Format | Location |
|---|---|
| **Excel** | `test-cases/User_Management_Test_Cases.xlsx` |
| **Markdown** | `test-cases/manual-test-cases.md` |

### 10 Test Cases Summary:

| ID | Test Case | Priority | Status |
|---|---|---|---|
| TC_001 | Login and Navigate to Admin Module | High | ✅ Pass |
| TC_002 | Add a New System User | High | ✅ Pass |
| TC_003 | Search the Newly Created User | High | ✅ Pass |
| TC_004 | Edit User Details (Role, Status, Username) | High | ✅ Pass |
| TC_005 | Validate Updated User Details | High | ✅ Pass |
| TC_006 | Delete the User | High | ✅ Pass |
| TC_007 | Form Validation — Empty Fields | Medium | ✅ Pass |
| TC_008 | Duplicate Username Validation | Medium | ✅ Pass |
| TC_009 | Password Mismatch Validation | Medium | ✅ Pass |
| TC_010 | Reset Button Clears Search Form | Low | ✅ Pass |

---

## 🖥️ Running Problem Statement 2 — Health Monitor Scripts

### Script 1: System Health Monitor

**What it does:**
Checks your computer's **CPU usage**, **Memory (RAM) usage**, **Disk space**, and lists the **top running processes**.
If any metric goes above 80%, it logs an **ALERT**.

**How to run:**
```powershell
python problem-statement-2/system_health_monitor.py
```

**Sample Output:**
```
2026-06-24 13:16:03 | INFO  | System Health Check
2026-06-24 13:16:04 | INFO  | CPU Usage: 16.0%  (Threshold: 80.0%) ✓
2026-06-24 13:16:04 | INFO  | Memory Usage: 82.3% (Used: 12.88 GB)
2026-06-24 13:16:04 | ALERT | Memory usage is above threshold!
2026-06-24 13:16:04 | INFO  | Disk Usage: 45.2% (Threshold: 90.0%) ✓
```

Logs are saved to: `logs/system_health.log`

---

### Script 2: Application Health Checker

**What it does:**
Sends an HTTP request to each website in the list and checks if it responds successfully (**UP**) or fails (**DOWN**). Shows the response time in milliseconds.

**How to run:**
```powershell
python problem-statement-2/app_health_checker.py
```

**Run with custom URLs:**
```powershell
python problem-statement-2/app_health_checker.py https://example.com https://google.com
```

**Sample Output:**
```
[UP]   | https://opensource-demo.orangehrmlive.com | HTTP 200 | 651ms
[UP]   | https://google.com                        | HTTP 200 | 123ms
[DOWN] | https://this-site-does-not-exist.com      | Connection Error
```

Logs are saved to: `logs/app_health.log`

---

## 🔄 GitHub Actions — Automatic CI/CD

This project has a **GitHub Actions workflow** (`.github/workflows/playwright-tests.yml`).

**What it does automatically:**
1. Every time you push code to GitHub → tests run automatically in the cloud
2. Sets up Python 3.11
3. Installs all dependencies
4. Installs Playwright Chromium
5. Runs all 6 tests
6. Uploads the HTML report as a downloadable artifact

**How to see it:**
1. Go to your GitHub repository
2. Click the **"Actions"** tab
3. You'll see each run with pass/fail status

---

## 🐛 Bugs & Issues Found During Testing

| Bug | Description | Resolution |
|---|---|---|
| **Autocomplete timing** | The Employee Name autocomplete showed a "Searching..." placeholder. Clicking too fast selected it instead of the actual employee, causing a validation error. | Fixed by waiting for the placeholder to disappear before clicking the result. |
| **Demo site slow loads** | The public OrangeHRM demo site is shared by many users and sometimes responds slowly (5–15 seconds), causing test timeouts. | Fixed by switching from `networkidle` to `domcontentloaded` strategy and increasing timeouts. Also switched to direct URL navigation instead of menu clicks. |

---

## 📊 Test Results Summary

| Metric | Value |
|---|---|
| Total Test Cases | 6 automated + 10 manual |
| Automated Tests Passed | **6 / 6 (100%)** |
| Manual Tests | 10 / 10 (all documented) |
| Browser Tested | Chromium |
| Average Run Time | ~60 seconds |
| Test Framework | pytest + Playwright |

---

## 🗂️ Submission Checklist

- [x] Manual Test Cases (Excel + Markdown)
- [x] Playwright Automation Code (6 test cases)
- [x] Page Object Model architecture
- [x] Screenshots (16 evidence screenshots)
- [x] HTML Test Report
- [x] Problem Statement 2 — System Health Monitor
- [x] Problem Statement 2 — App Health Checker
- [x] GitHub Actions CI/CD pipeline
- [x] README documentation
- [x] requirements.txt for easy setup

---

## 👤 Author

**Surya M**
AccuKnox QA Trainee Practical Assessment Submission

---

## 📄 License

This project is created solely for the AccuKnox QA Trainee Practical Assessment.
