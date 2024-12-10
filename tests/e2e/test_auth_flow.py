# e2e test: Auth flow

from playwright.sync_api import sync_playwright


def test_user_registration():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Deploy in headless mode
        page = browser.new_page()

        # Go to register page
        page.goto("http://localhost:5000/register")

        # Fill the register form
        page.fill("input[name='username']", "testuser")
        page.fill("input[name='password']", "password")
        page.click("button[type='submit']")

        # Verify redirection to login page
        assert "User Login" in page.title()

        browser.close()
