from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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

class SigninGoogle:
    def test_TCA1008_SIGNIN_GOOGLE(self, driver):
        """TCA1008_SIGNIN_GOOGLE: Sign in using Google credential"""
        print("Begin TCA1008_SIGNIN_GOOGLE test execution...")

        account = wait_for_element(driver, (AppiumBy.ACCESSIBILITY_ID, "Account"))
        account.click()

        time.sleep(3)

        navigate_login = wait_for_element(driver, (AppiumBy.ANDROID_UIAUTOMATOR,"new UiSelector().className(\"android.widget.Button\").instance(0)"))
        navigate_login.click()

        time.sleep(3)

        continue_with_google = wait_for_element(driver, (AppiumBy.ID,
                                                   "com.photobook.android.staging:id/googleButton"))
        continue_with_google.click()

        select_gmail_account = wait_for_element(driver, (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().className(\"android.widget.LinearLayout\").instance(3)"))
        select_gmail_account.click()

        time.sleep(20)
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(764, 1596)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        time.sleep(7)
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(758, 2100)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        print("Successfully logged in!")
        time.sleep(3)
