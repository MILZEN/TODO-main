from selenium import webdriver

def test_user_registration():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")
    driver.find_element("name", "username").send_keys("testuser")
    driver.find_element("name", "password").send_keys("password")
    driver.find_element("name", "submit").click()
    assert "Login" in driver.title
    driver.quit()
