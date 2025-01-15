import subprocess
import time
from asyncio import timeout

from appium import webdriver
from typing import Any, Dict
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
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

class LilphotobookPurchase:
    def test_TCA1006_LILPHOTOBOOK_PURCHASE(self, driver):

        # Wait and interact with elements
        home = wait_for_element(driver, (AppiumBy.ACCESSIBILITY_ID, "Home"))
        home.click()

        view_more = wait_for_element(driver,(AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"View More\").instance(0)"))
        view_more.click()

        print("Buying Lil' Photobook...")
        lil_photobook = wait_for_element(driver, (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"Lil' Photobook\")"))
        lil_photobook.click()

        next_button = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/action_product_next"))
        next_button.click()

        print("Adding pictures...")
        wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/albumConstraintLayout"))
        open_gallery = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/albumConstraintLayout"))
        open_gallery.click()

        select_all_pictures = wait_for_element(driver, (
        AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().className(\"android.widget.FrameLayout\").instance(22)"))
        select_all_pictures.click()

        continue_button = wait_for_element(driver,(AppiumBy.ID, "com.photobook.android.staging:id/continueWithPhotoCountButton"))
        continue_button.click()

        print("Adding project to cart...")
        add_to_cart_button_small = wait_for_element(driver, (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"Add to cart\")"))
        add_to_cart_button_small.click()

        time.sleep(2)
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(1003, 1448)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        all_good_button = wait_for_element(driver,(AppiumBy.ID, "com.photobook.android.staging:id/verticalDialogCancelButton"))
        all_good_button.click()

        print("Begin checkout process...")
        checkout = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/checkoutButton"))
        checkout.click()

        select_payment_method_button = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/selectPaymentMethodButton"))
        select_payment_method_button.click()

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(502, 2033)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(534, 326)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        choose_payment_method = wait_for_element(driver, (
        AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"Offline Payment\")"))
        choose_payment_method.click()

        select_payment_button = wait_for_element(driver,(AppiumBy.ID, "com.photobook.android.staging:id/selectPaymentButton"))
        select_payment_button.click()

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(515, 1735)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(518, 473)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        order_now_button = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/orderNowButton"))
        order_now_button.click()

        print("Order completed!")
        view_my_order = wait_for_element(driver,(AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().resourceId(\"view_my_orders\")"))
        view_my_order.click()

        print("Navigate to Account page...")
        back_button = wait_for_element(driver, (AppiumBy.CLASS_NAME, "android.widget.Button"))
        back_button.click()

    # Note: Make sure to navigate back to Account page to initiate logout process
    ######### ENDING POINT ###########

