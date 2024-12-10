# e2e test: Task flow

from playwright.sync_api import sync_playwright
import time


def test_register_and_create_task():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # User register
        page.goto("http://localhost:5000/register")
        page.fill("input[name='username']", "testuser")
        page.fill("input[name='email']", "testuser@example.com")
        page.fill("input[name='password']", "testpassword")
        page.fill("input[name='first_name']", "Test")
        page.fill("input[name='last_name']", "User")
        page.click("button[type='submit']")
        # Wait redirection to home page
        page.wait_for_url("http://localhost:5000/")

        # Create task
        page.fill("input[name='title']", "Test Task")
        page.fill("select[name='priority']", "High")
        page.click("button[type='submit']")

        # Wait the tasks list
        page.wait_for_selector("ul#task-list li")

        # Verify created task
        assert "Test Task" in page.content()

        browser.close()


def test_edit_and_delete_task():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Login to obtain the home URL with the username
        page.goto("http://localhost:5000/login")
        page.fill("input[name='email']", "testuser@example.com")  # Use valid email
        page.fill("input[name='password']", "testpassword")
        page.click("button[type='submit']")
        page.wait_for_load_state("load")

        page.wait_for_selector("h1")

        username = "testuser"  # Must be equal than username after login
        page.goto(f"http://localhost:5000/home/{username}")

        # Edit task
        task = page.locator("text=Test Task")
        task.click()
        page.click("button:has-text('Edit')")
        page.fill("input[name='title']", "Updated Task")
        page.click("button[type='submit']")
        time.sleep(2)  # Wait update

        # Verify updated task
        assert "Updated Task" in page.content()

        # Delete task
        page.click("button:has-text('Delete')")
        time.sleep(2)  # Wait deletion

        # Verifydeleted task
        assert "Updated Task" not in page.content()

        browser.close()
