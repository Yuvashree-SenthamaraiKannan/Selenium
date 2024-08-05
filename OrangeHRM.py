import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()

driver.implicitly_wait(10)
def login(username, password):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.maximize_window()
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)

    submit_button = WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
    )
    submit_button.click()


def test_positive_login():
    login("Admin", "admin123")
    time.sleep(3)
    assert "OrangeHRM" in driver.title
    print("Positive test passed: Successfully logged in with valid credentials.")


def test_negative_login():
    login("Admin", "Admin1234")
    login("Yuvashree" , "admin123")
    try:
        error_message_element = WebDriverWait(driver, 30).until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//div[@class="oxd-alert-content oxd-alert-content--error"]'))
        )
        error_message = error_message_element.text
        assert "Invalid credentials" in error_message
        print("Negative test passed: Login failed with invalid credentials.")
    except Exception as e:
        print(f"Negative test failed: {e}")


def main():
    try:
        test_negative_login()
        test_positive_login()
    finally:
        driver.quit()


if __name__ == "__main__":
    main()



