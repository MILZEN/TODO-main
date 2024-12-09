# Prueba de task
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pytest
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    yield driver
    driver.quit()

def test_register_and_create_task(driver):
    # Paso 1: Registrar usuario
    driver.get("http://localhost:5000/register")
    driver.find_element(By.NAME, "username").send_keys("testuser")
    driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "password").send_keys("testpassword")
    driver.find_element(By.NAME, "first_name").send_keys("Test")
    driver.find_element(By.NAME, "last_name").send_keys("User")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)  # Esperar redirección

    # Paso 2: Crear tarea
    driver.find_element(By.XPATH, "//button[contains(text(), 'Add Task')]").click()
    driver.find_element(By.NAME, "title").send_keys("Test Task")
    driver.find_element(By.NAME, "priority").send_keys("High")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)  # Esperar creación

    # Verificar tarea creada
    assert "Test Task" in driver.page_source

def test_edit_and_delete_task(driver):
    # Paso 1: Editar tarea
    driver.get("http://localhost:5000/home/testuser")
    task = driver.find_element(By.XPATH, "//div[contains(text(), 'Test Task')]")
    task.click()
    driver.find_element(By.XPATH, "//button[contains(text(), 'Edit')]").click()
    driver.find_element(By.NAME, "title").clear()
    driver.find_element(By.NAME, "title").send_keys("Updated Task")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)  # Esperar actualización

    # Verificar actualización
    assert "Updated Task" in driver.page_source

    # Paso 2: Eliminar tarea
    driver.find_element(By.XPATH, "//button[contains(text(), 'Delete')]").click()
    time.sleep(2)  # Esperar eliminación

    # Verificar que la tarea fue eliminada
    assert "Updated Task" not in driver.page_source