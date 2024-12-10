# e2e test: Task flow

from playwright.sync_api import sync_playwright
import time


def test_register_and_create_task():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Registro de usuario
        page.goto("http://localhost:5000/register")
        page.fill("input[name='username']", "testuser")
        page.fill("input[name='email']", "testuser@example.com")
        page.fill("input[name='password']", "testpassword")
        page.fill("input[name='first_name']", "Test")
        page.fill("input[name='last_name']", "User")
        page.click("button[type='submit']")
        # Esperar redirección a la home page
        page.wait_for_url("http://localhost:5000/")

        # Crear tarea (esperar que el input de tarea esté disponible)
        page.fill("input[name='title']", "Test Task")
        page.fill("select[name='priority']", "High")
        page.click("button[type='submit']")

        # Espera hasta que se cargue la lista de tareas
        page.wait_for_selector("ul#task-list li")

        # Verificar tarea creada
        assert "Test Task" in page.content()

        browser.close()


def test_edit_and_delete_task():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Iniciar sesión para obtener la URL de home con el username del usuario
        page.goto("http://localhost:5000/login")
        page.fill("input[name='email']", "testuser@example.com")  # Use valid email
        page.fill("input[name='password']", "testpassword")
        page.click("button[type='submit']")
        # Esperar a que la página se cargue correctamente
        page.wait_for_load_state("load")

        # Esperar que la página home esté lista
        page.wait_for_selector("h1")

        # Acceder a la página del usuario en home
        username = "testuser"  # Must be equal than username after login
        page.goto(f"http://localhost:5000/home/{username}")

        # Editar tarea
        task = page.locator("text=Test Task")
        task.click()
        page.click("button:has-text('Edit')")
        page.fill("input[name='title']", "Updated Task")
        page.click("button[type='submit']")
        time.sleep(2)  # Esperar actualización

        # Verificar tarea actualizada
        assert "Updated Task" in page.content()

        # Eliminar tarea
        page.click("button:has-text('Delete')")
        time.sleep(2)  # Esperar eliminación

        # Verificar tarea eliminada
        assert "Updated Task" not in page.content()

        browser.close()
