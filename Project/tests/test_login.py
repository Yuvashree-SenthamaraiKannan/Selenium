import time
import logging
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Configure logging
logging.basicConfig(filename='logs/test_login.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class TestOrangeHRM:
    def __init__(self):
        # Load configuration and locators
        with open('C:/Users/ykannan/PycharmProjects/Project/config/config.yaml', 'r') as config_file:
            self.config = yaml.safe_load(config_file)

        with open('C:/Users/ykannan/PycharmProjects/Project/locators/locators.yaml', 'r') as locators_file:
            self.locators = yaml.safe_load(locators_file)

        # Initialize WebDriver
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.base_url = self.config['default']['url']

    def login(self, username, password):
        """Method to perform login."""
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        logging.info("Navigated to OrangeHRM login page.")

        self.driver.find_element(By.XPATH, self.locators['login_page']['username_xpath']).send_keys(username)
        self.driver.find_element(By.XPATH, self.locators['login_page']['password_xpath']).send_keys(password)

        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.locators['login_page']['submit_button_xpath']))
        )
        submit_button.click()
        logging.info(f"Attempted to login with username: {username}")

    def test_positive_login(self):
        """Test case for successful login."""
        try:
            self.login(self.config['default']['username'], self.config['default']['password'])
            time.sleep(3)  # Wait for the page to load
            assert "OrangeHRM" in self.driver.title
            logging.info("Positive test passed: Successfully logged in with valid credentials.")
        except AssertionError:
            logging.error("Positive test failed: Failed to log in with valid credentials.")
            raise

    def test_negative_login(self):
        """Test case for unsuccessful login."""
        try:
            self.login("Admin", "Admin1234")  # Incorrect password
            self.login("Yuvashree", "admin123")  # Incorrect username

            error_message_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, self.locators['login_page']['error_message_xpath']))
            )
            error_message = error_message_element.text
            assert "Invalid credentials" in error_message
            logging.info("Negative test passed: Login failed with invalid credentials.")
        except AssertionError:
            logging.error("Negative test failed: Did not receive expected error message.")
            raise
        except Exception as e:
            logging.error(f"Negative test failed: {e}")
            raise

    def run_tests(self):
        """Run all test cases."""
        try:
            self.test_negative_login()
            self.test_positive_login()
        finally:
            self.driver.quit()
            logging.info("Driver closed.")


if __name__ == "__main__":
    test_suite = TestOrangeHRM()
    test_suite.run_tests()
