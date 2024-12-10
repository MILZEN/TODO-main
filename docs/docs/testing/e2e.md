# End-to-End (E2E) Tests Documentation

This document describes the End-to-End (E2E) tests implemented for the application. E2E tests ensure that the application behaves as expected from the user's perspective, covering workflows like registration, task creation, editing, and deletion.

## Auth Flow E2E Test (`test_auth_flow.py`)

### `test_user_registration`
- **Description**: This test simulates a user registration flow, checking that a user can successfully register and is redirected to the login page.
- **Test Logic**:
    - The test uses Playwright to open a Chromium browser in headless mode.
    - The test navigates to the registration page, fills in the registration form with user details, and submits the form.
    - After submitting the form, the test verifies that the user is redirected to the login page by checking if the page title contains `"User Login"`.
- **Expected Outcome**: The user should be successfully registered, and the browser should redirect to the login page.
  
    ```python
    def test_user_registration():
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Launching in headless mode
            page = browser.new_page()

            # Go to the registration page
            page.goto("http://localhost:5000/register")

            # Fill the registration form
            page.fill("input[name='username']", "testuser")
            page.fill("input[name='password']", "password")
            page.click("button[type='submit']")

            # Verify redirection to the login page
            assert "User Login" in page.title()  # Verify the title is "Login"

            browser.close()
    ```

## Task Flow E2E Tests (`test_task_flow.py`)

### `test_register_and_create_task`
- **Description**: This test covers the process of registering a new user and then creating a task.
- **Test Logic**:
    - The test navigates to the registration page and fills in the registration form.
    - After the user is registered and redirected to the home page, the test creates a new task by filling in the title and priority fields and submitting the form.
    - After submission, the test waits for the task list to update and verifies that the newly created task is visible on the page.
- **Expected Outcome**: The user should be able to create a task successfully, and the task should appear in the task list.
  
    ```python
    def test_register_and_create_task():
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Register a new user
            page.goto("http://localhost:5000/register")
            page.fill("input[name='username']", "testuser")
            page.fill("input[name='email']", "testuser@example.com")
            page.fill("input[name='password']", "testpassword")
            page.fill("input[name='first_name']", "Test")
            page.fill("input[name='last_name']", "User")
            page.click("button[type='submit']")
            # Wait for redirection to the home page
            page.wait_for_url("http://localhost:5000/")

            # Create a new task (wait for task input to be available)
            page.fill("input[name='title']", "Test Task")
            page.fill("select[name='priority']", "High")
            page.click("button[type='submit']")

            # Wait for the task list to update
            page.wait_for_selector("ul#task-list li")

            # Verify that the task was created
            assert "Test Task" in page.content()

            browser.close()
    ```

### `test_edit_and_delete_task`
- **Description**: This test verifies that a user can edit and delete a task after logging in.
- **Test Logic**:
    - The test starts by logging in with a previously registered user.
    - After logging in, it navigates to the user's home page and locates an existing task.
    - The test edits the task by changing its title and submits the changes, then verifies that the task has been updated.
    - It then deletes the task and verifies that the task no longer exists in the task list.
- **Expected Outcome**: The task should be updated and deleted successfully, with the changes reflected on the page.
  
    ```python
    def test_edit_and_delete_task():
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Log in to the application
            page.goto("http://localhost:5000/login")
            page.fill("input[name='email']", "testuser@example.com")  # Use valid email
            page.fill("input[name='password']", "testpassword")
            page.click("button[type='submit']")
            # Wait for the page to load completely
            page.wait_for_load_state("load")

            # Wait for the home page to be ready
            page.wait_for_selector("h1")

            # Go to the user's home page
            username = "testuser"  # Must match the username after login
            page.goto(f"http://localhost:5000/home/{username}")

            # Edit the task
            task = page.locator("text=Test Task")
            task.click()
            page.click("button:has-text('Edit')")
            page.fill("input[name='title']", "Updated Task")
            page.click("button[type='submit']")
            time.sleep(2)  # Wait for the update

            # Verify that the task was updated
            assert "Updated Task" in page.content()

            # Delete the task
            page.click("button:has-text('Delete')")
            time.sleep(2)  # Wait for the deletion

            # Verify that the task was deleted
            assert "Updated Task" not in page.content()

            browser.close()
    ```

---

### Summary

The End-to-End tests simulate real user interactions with the application, ensuring that registration, task creation, task editing, and task deletion work as expected. These tests cover the full flow of the application and validate the most critical user actions.
