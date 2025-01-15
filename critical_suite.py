import os
import sys
import time
from datetime import datetime
from typing import Any, Dict

import allure
import pytest
from allure_commons.types import Severity
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Critical.TCA1006_LILPHOTOBOOK_PURCHASE import LilphotobookPurchase
from Critical.TCA1008_SIGNIN_GOOGLE import SigninGoogle

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Critical.TCA1005_SIMPLEBOOK_PURCHASE import SimplebookPurchase


# Global variables
appium_service = None
driver = None


def take_screenshot(name: str):
    """Take a screenshot and attach it to the Allure report"""
    if driver:
        try:
            # Create screenshots directory if it doesn't exist
            screenshot_dir = os.path.join(os.getcwd(), 'screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)

            # Take screenshot with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)

            driver.save_screenshot(filepath)

            # Attach to Allure report
            allure.attach.file(filepath, name=filename, attachment_type=allure.attachment_type.PNG)
            print(f"Screenshot saved: {filepath}")
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")

def wait_for_element(driver, locator, timeout=60):
    """Wait for an element to be present and visible"""
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(EC.presence_of_element_located(locator))
        wait.until(EC.visibility_of(element))
        return element
    except TimeoutException:
        print(f"Timeout waiting for element: {locator}")
        return None

def restart_app():
    """Restart the app using the driver"""
    global driver
    if driver:
        try:
            driver.terminate_app('com.photobook.android.staging')
            time.sleep(2)
            driver.activate_app('com.photobook.android.staging')
            time.sleep(3)  # Wait for app to launch
        except Exception as e:
            print(f"Error restarting app: {str(e)}")

@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    global appium_service, driver

    # Start Appium service
    appium_service = AppiumService()
    appium_service.start()

    # Appium capabilities
    cap: Dict[str, Any] = {
        'platformName': "Android",
        'automationName': "UiAutomator2",
        'deviceName': "emulator-5554",
        'appPackage': "com.photobook.android.staging",
        'appActivity': "com.photobook.android.page.applaunch.AppLaunchActivity",
        'noReset': False,
        'autoGrantPermissions': True
    }

    # Initialize driver with options
    url = 'http://127.0.0.1:4723'
    options = AppiumOptions().load_capabilities(cap)
    driver = webdriver.Remote(url, options=options)

    yield driver

    # Teardown
    if driver:
        driver.quit()
    if appium_service:
        appium_service.stop()

@pytest.fixture(autouse=True)
def restart_app_before_test():
    """Fixture to restart app before each test"""
    restart_app()
    yield

class TestPhotobook:
    """Test class containing all Critical-priority test cases"""
    def select_country(self):
        select_country = wait_for_element(driver,
                                          (AppiumBy.ID, "com.photobook.android.staging:id/countryArrowImageView"))
        select_country.click()
        select_country.click()

        # Search for Malaysia
        search_bar = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/search_bar"))
        search_bar.click()

        country_name = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/search_src_text"))
        country_name.send_keys("Malaysia")

        # Select Malaysia and continue
        select_malaysia = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/pickerTextView"))
        select_malaysia.click()

        continue_btn = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/continueButton"))
        continue_btn.click()

        # Navigate to Home
        el7 = wait_for_element(driver, (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"View More\")"))
        el7.click()

        el8 = wait_for_element(driver, (AppiumBy.ACCESSIBILITY_ID, "Home"))
        el8.click()

    def signup_user(self, first_name, last_name, email, password):
        print("Begin TCA1001_SIGNUP test execution...")
        account = wait_for_element(driver, (AppiumBy.ACCESSIBILITY_ID, "Account"))
        account.click()

        time.sleep(3)

        navigate_login = wait_for_element(driver, (AppiumBy.ANDROID_UIAUTOMATOR,
                                             "new UiSelector().className(\"android.widget.Button\").instance(0)"))
        navigate_login.click()

        time.sleep(5)
        # Clicking Sign Up
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(937, 1506)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        # Filling sign up details
        first_name_field = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/firstNameEditText"))
        first_name_field.click()
        first_name_field.send_keys(first_name)

        last_name_field = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/lastNameEditText"))
        last_name_field.click()
        last_name_field.send_keys(last_name)

        email_field = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/emailEditText"))
        email_field.click()
        email_field.send_keys(email)

        time.sleep(2)
        # Scrolling down
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(770, 1308)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(776, 408)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        password_field = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/passwordEditText"))
        password_field.click()
        password_field.send_keys(password)

        # Signing up...
        sign_up_button = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/signUpButton"))
        sign_up_button.click()

        print("Successfully registered an account!")

        time.sleep(3)


    def login_user(self, email, password):
        """Common login function"""
        print(f"Logging in with email: {email}")

        account = wait_for_element(driver, (AppiumBy.ACCESSIBILITY_ID, "Account"))
        account.click()

        time.sleep(3)

        navigate_login = wait_for_element(driver, (AppiumBy.ANDROID_UIAUTOMATOR,
                                                   "new UiSelector().className(\"android.widget.Button\").instance(0)"))
        navigate_login.click()

        time.sleep(3)

        email_field = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/emailEditText"))
        email_field.click()
        email_field.send_keys(email)

        password_field = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/passwordEditText"))
        password_field.click()
        password_field.send_keys(password)

        login_button = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/loginButton"))
        login_button.click()

        time.sleep(3)


    def logout_user(self):
        """Common logout function"""
        print("Logging out...")
        time.sleep(7)

        # Scroll to logout button
        for _ in range(5):
            driver.execute_script('mobile: scrollGesture', {
                'left': 100,
                'top': 1000,
                'width': 200,
                'height': 1000,
                'direction': 'down',
                'percent': 1.0
            })
            time.sleep(1)

        logout_button = wait_for_element(driver, (AppiumBy.ANDROID_UIAUTOMATOR,
                                                  "new UiSelector().className(\"android.widget.Button\").instance(10)"))
        logout_button.click()

        time.sleep(1)
        logout_okay_button = wait_for_element(driver,
                                              (
                                              AppiumBy.ID, "com.photobook.android.staging:id/verticalDialogOkayButton"))
        logout_okay_button.click()
        print("Successfully logged out!")
        time.sleep(2)


    @pytest.mark.test_id("TCA1002_LOGIN")
    @allure.severity(Severity.CRITICAL)
    def test_TCA1002_LOGIN(self):
        """TCA1002_LOGIN : Login into PB App"""
        try:
            print("Begin TCA1002_LOGIN test execution...")
            self.select_country()
            self.login_user("autobots_ui_login@photobookworldwide.com", "Testing@123")
            self.logout_user()
            print("TCA1002_LOGIN test execution completed successfully!")
        except Exception as e:
            take_screenshot("TCA1002_LOGIN_failure")
            pytest.fail(f"TCA1002_LOGIN failed: {str(e)}")


    @pytest.mark.test_id("TCA1005_SIMPLEBOOK_PURCHASE")
    @allure.severity(Severity.CRITICAL)
    def test_TCA1005_SIMPLEBOOK_PURCHASE(self):
        """TCA1005_SIMPLEBOOK_PURCHASE: Buying Simplebook test"""
        try:
            print("Begin TCA1005_SIMPLEBOOK_PURCHASE test execution...")
            self.login_user("autobots_ui_buybook@photobookworldwide.com", "Testing@123")
            simplebook_purchase = SimplebookPurchase()
            simplebook_purchase.test_TCA1005_SIMPLEBOOK_PURCHASE(driver)
            self.logout_user()
            print("TCA1005_SIMPLEBOOK_PURCHASE test execution completed successfully!")
        except Exception as e:
            take_screenshot("TCA1005_SIMPLEBOOK_PURCHASE_failure")
            pytest.fail(f"TCA1005_SIMPLEBOOK_PURCHASE failed: {str(e)}")

    @pytest.mark.test_id("TCA1006_LILPHOTOBOOK_PURCHASE")
    @allure.severity(Severity.CRITICAL)
    def test_TCA1006_LILPHOTOBOOK_PURCHASE(self):
        """TCA1006_LILPHOTOBOOK_PURCHASE: Buying Lil'Photobook test"""
        try:
            print("Begin TCA1006_LILPHOTOBOOK_PURCHASE test execution...")
            self.login_user("autobots_ui_lilphotobook@photobookworldwide.com", "Testing@123")
            lilphotobook_purchase = LilphotobookPurchase()
            lilphotobook_purchase.test_TCA1006_LILPHOTOBOOK_PURCHASE(driver)
            self.logout_user()
            print("TCA1006_LILPHOTOBOOK_PURCHASE test execution completed successfully!")
        except Exception as e:
            take_screenshot("TCA1006_LILPHOTOBOOK_PURCHASE_failure")
            pytest.fail(f"TCA1006_LILPHOTOBOOK_PURCHASE failed: {str(e)}")


    @pytest.mark.test_id("TCA1008_SIGNIN_GOOGLE")
    @allure.severity(Severity.CRITICAL)
    def test_TCA1008_SIGNIN_GOOGLE(self):
        """TCA1008_SIGNIN_GOOGLE : Login using Google credential"""
        try:
            google_signin = SigninGoogle()
            google_signin.test_TCA1008_SIGNIN_GOOGLE(driver)  # Pass driver as argument
            self.logout_user()
            print("TCA1008_SIGNIN_GOOGLE test execution completed successfully!")
        except Exception as e:
            take_screenshot("TCA1008_SIGNIN_GOOGLE_failure")
            pytest.fail(f"TCA1008_SIGNIN_GOOGLE failed: {str(e)}")

if __name__ == "__main__":
    # Run all tests by default
    pytest.main(["-v", "--alluredir=/app/allureReport", __file__])


    # Or run all tests
    # pytest.main(["-v", __file__])