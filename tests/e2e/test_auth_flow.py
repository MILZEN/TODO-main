# e2e test: Auth flow 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_user_registration():
    # Configuration to use Chrome in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Execute without interface
    chrome_options.add_argument("--no-sandbox")  # Avoid sandbox issues
    chrome_options.add_argument("--disable-dev-shm-usage")  # Fix memory issues

    # Use Service to specify ChromeDriver location
    service = Service(ChromeDriverManager().install())

    # Init in headless mode
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("http://localhost:5000/register")
    driver.find_element("name", "username").send_keys("testuser")
    driver.find_element("name", "password").send_keys("password")
    driver.find_element("name", "submit").click()
    assert "Login" in driver.title
    driver.quit()