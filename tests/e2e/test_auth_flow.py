# e2e test: Auth flow 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_user_registration():
    # Configuration to run Chrome in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without interface
    chrome_options.add_argument("--no-sandbox")  # Avoid sandbox issues
    chrome_options.add_argument("--disable-dev-shm-usage")  # Fix memory issues

    # Use Service to specify the location of ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Initialize in headless mode
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Make sure the Selenium container is running at the correct URL
    selenium_url = "http://localhost:4444/wd/hub"
    driver = webdriver.Remote(
        command_executor=selenium_url,
        options=chrome_options
    )

    # Perform the registration test
    driver.get("http://localhost:5000/register")
    driver.find_element("name", "username").send_keys("testuser")
    driver.find_element("name", "password").send_keys("password")
    driver.find_element("name", "submit").click()

    # Verify that after registration, the page redirects to the login page
    assert "Login" in driver.title

    # Close the browser after the test
    driver.quit()