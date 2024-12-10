# e2e test: Auth flow

from playwright.sync_api import sync_playwright


def test_user_registration():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Lanzar en modo headless
        page = browser.new_page()

        # Ir a la página de registro
        page.goto("http://localhost:5000/register")

        # Completar el formulario de registro
        page.fill("input[name='username']", "testuser")
        page.fill("input[name='password']", "password")
        page.click("button[type='submit']")

        # Verificar redirección a la página de login
        assert "User Login" in page.title()  # Verificar que el título es "Login"

        browser.close()
