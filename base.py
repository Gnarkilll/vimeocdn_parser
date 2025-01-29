from datetime import datetime as dt
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from waiting_module.waiter import wait_for_visible, wait_for_attr_contains_text, wait_for_alert_is_present, \
    TimeoutException


class BPLocators:
    EMAIL_INPUT = By.CLASS_NAME, "login"
    PASSWORD_INPUT = By.CLASS_NAME, "password"
    LOGIN_BUTTON = By.CLASS_NAME, "main-button"


class BasePage:

    app_counter = 0

    def __init__(self, driver):
        self.driver = driver


    def start_app(self):
        self.driver.get(self.base_url)
        wait_for_visible(self.driver, BPLocators.EMAIL_INPUT)
        self.set_value(BPLocators.EMAIL_INPUT, "jlr.rugandhar")
        self.set_value(BPLocators.PASSWORD_INPUT, "S!Lv3rStone")
        self.click(BPLocators.LOGIN_BUTTON)
        wait_for_visible(self.driver, BPLocators.INCONTROL_ROUTE_PLANNER_TEXT)

    def open(self, page_url=None):
        self.driver.get(page_url)

    def get_current_url(self):
        print("Get current URL")
        current_url = self.driver.current_url
        print(f"Current URL: {current_url}")
        return current_url

    def get_current_title(self):
        print("Get current title")
        current_title = self.driver.title
        print(f"Current title: {current_title}")
        return current_title

    def click(self, locator, **kwargs):
        print(f"Click by {locator}")
        self.get_element(locator, **kwargs).click()

    def is_locator_or_web_element(self, locator, **kwargs):
        return self.get_element(locator, **kwargs) if isinstance(locator, tuple) else locator

    def js_click(self, locator, **kwargs):
        print(f"JS click by {locator}")
        element = self.is_locator_or_web_element(locator, **kwargs)
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_to_element(self, locator, **kwargs):
        print(f"Scroll to {locator}")
        element = self.is_locator_or_web_element(locator, **kwargs)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def js_set_value(self, locator, value, **kwargs):
        print(f"JS set value '{value}' for {locator}")
        element = self.is_locator_or_web_element(locator, **kwargs)
        self.driver.execute_script(f"arguments[0].value='{value}'", element)

    def set_value(self, locator, value_to_set, **kwargs):
        print(f"Set value '{value_to_set}' for {locator}")
        wait_for_visible(self.driver, locator)
        self.clear(locator)
        self.js_set_value(locator, value_to_set, **kwargs)
        wait_for_attr_contains_text(self.driver, locator, attr="value", text=value_to_set)
        return value_to_set

    def set_text(self, locator, text, **kwargs):
        print(f"Set text '{text}' for {locator}")
        self.get_element(locator, **kwargs).send_keys(text)

    def clear(self, locator, **kwargs):
        print(f"Clear input field for {locator}")
        self.get_element(locator, **kwargs).clear()

    def press_keyboard_key(self, locator, key, **kwargs):
        key_name = next((k for k, v in Keys.__dict__.items() if key == v), None)
        print(f"Press key '{key_name}' for {locator}")
        self.get_element(locator, **kwargs).send_keys(key)

    def get_text(self, locator, **kwargs):
        print(f"Get text for {locator}")
        text = self.get_element(locator, **kwargs).text
        print(f"Retrieved text value: {text}")
        return text

    def is_selected(self, locator, **kwargs):
        print(f"Check element {locator} is selected")
        return self.get_element(locator, **kwargs).is_selected()

    def is_displayed(self, locator, **kwargs):
        print(f"Check element {locator} is displayed")
        return self.get_element(locator, **kwargs).is_displayed()

    def is_enabled(self, locator, **kwargs):
        print(f"Check element {locator} is enabled")
        return self.get_element(locator, **kwargs).is_enabled()

    def get_attribute(self, locator, attribute, **kwargs):
        print(f"Get attribute for {locator}")
        attr = self.get_element(locator, **kwargs).get_attribute(attribute)
        print(f"Retrieved attribute value: {attr}")
        return attr

    def get_all_attributes(self, locator, **kwargs):
        element = self.is_locator_or_web_element(locator, **kwargs)
        return self.driver.execute_script('var items = {}; for (index = 0; index < '
                                          'arguments[0].attributes.length; ++index) '
                                          '{ items[arguments[0].attributes[index].name] = '
                                          'arguments[0].attributes[index].value }; return items;', element)

    def get_css_property_value(self, locator, css_property, **kwargs):
        print(f"Get CSS property value for {locator}")
        if "color" in css_property:
            value = to_rgb(self.get_element(locator, **kwargs).value_of_css_property(css_property))
            print(f"Retrieved CSS property value: {value}")
            return value
        else:
            value = self.get_element(locator, **kwargs).value_of_css_property(css_property)
            print(f"Retrieved CSS property value: {value}")
            return value

    def exist(self, locator, **kwargs):
        print(f"Check element {locator} exists")
        try:
            self.get_element(locator, **kwargs)
        except NoSuchElementException:
            return False
        return True

    def get_element(self, locator, **kwargs):
        if "timeout" in kwargs.keys():
            start_to_wait = kwargs.get("timeout")
        else:
            start_to_wait = 3
        end_to_wait = 0
        start_time = dt.now()
        while end_to_wait < start_to_wait:
            try:
                if "element_index" in kwargs.keys():
                    return self.find_elements(locator)[kwargs.get("element_index")]
                else:
                    return self.find_element(locator)
            except NoSuchElementException:
                print(f"Wait for element exists: {locator}")
                end_to_wait = (dt.now() - start_time).seconds
                sleep(1)
        else:
            raise NoSuchElementException(f"Unable to find element: {locator}")

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def switch_browser_tab_to(self, window):
        print(f"Switch browser tab to: {window}")
        self.driver.switch_to.window(window)

    @property
    def get_all_tabs(self):
        print("Get browser tabs")
        return self.driver.window_handles

    def activate_checkbox(self, locator, **kwargs):
        print(f"Activate checkbox for {locator}")
        if not self.is_selected(locator, **kwargs):
            self.js_click(locator, **kwargs)
            assert self.is_selected(locator, **kwargs)
        else:
            print("Checkbox is already activated")

    def deactivate_checkbox(self, locator, **kwargs):
        print(f"Deactivate checkbox for {locator}")
        if self.is_selected(locator, **kwargs):
            self.js_click(locator, **kwargs)
            assert not self.is_selected(locator, **kwargs)
        else:
            print("Checkbox is already deactivated")

    def drag_and_drop(self, source_web_element, target_web_element):
        print(f"Drag&Drop from {source_web_element} to {target_web_element}")
        which_env = self.env_handler.__class__.__name__.lower()
        if CONTAINER.FIREFOX in self.driver.name and "common" in which_env:
            ActionChains(self.driver).drag_and_drop(source_web_element, target_web_element).perform()
        elif "osx" in which_env:
            ActionChains(self.driver).click_and_hold(source_web_element).send_keys(Keys.DOWN).release(
                target_web_element).perform()
        elif "ios" in which_env or "android" in which_env:
            TouchAction(self.driver).long_press(source_web_element, duration=5000).move_to(target_web_element).release().perform()
        else:
            ActionChains(self.driver).click_and_hold(source_web_element).pause(1)\
                .move_to_element(target_web_element).release(target_web_element).perform()

    def click_with_delay(self, locator, delay=3, **kwargs):
        print(f"Click by {locator} with delay {delay}sec")
        web_element = self.get_element(locator, **kwargs)
        ActionChains(self.driver).pause(delay).click(web_element).perform()

    def pause(self, seconds_to_pause=3):
        print(f"Pause execution: {seconds_to_pause}sec")
        ActionChains(self.driver).pause(seconds_to_pause).perform()

    def move_to_element(self, locator, **kwargs):
        print(f"Move to {locator}")
        web_element = self.get_element(locator, **kwargs)
        ActionChains(self.driver).move_to_element(web_element).perform()

    def make_screenshot(self, locator, shot_name, timeout=None, **kwargs):
        print(f"Make screenshot '{shot_name}' for {locator}")
        if timeout:
            self.pause_execution(timeout)
        self.get_element(locator, **kwargs).screenshot(f"{PATH.IMAGES_DIR}/{shot_name}.png")

    def make_full_screenshot(self, shot_name, timeout=None):
        print(f"Make full screenshot: {shot_name}")
        if timeout:
            self.pause_execution(timeout)
        self.driver.save_screenshot(f"{PATH.IMAGES_DIR}/{shot_name}.png")

    def check_alert_exists(self, timeout=3):
        print("Check alert popup exists")
        try:
            wait_for_alert_is_present(self.driver, timeout=timeout)
        except TimeoutException:
            return False
        return True

    @property
    def get_cookies(self):
        print("Get cookies")
        cookies = self.driver.get_cookies()
        print(f"Retrieved cookies: {cookies}")
        return cookies

    def mobile_swipe(self, locator, swipe_direction, **kwargs):
        print(f"Swipe element: {locator} to {swipe_direction.upper()}")
        element = self.is_locator_or_web_element(locator, **kwargs)
        self.driver.execute_script("mobile: swipe", {"direction": f"{swipe_direction}", "element": element})

    def perform_editor_action(self, action):
        print(f"Perform editor action: {action}")
        """
        :param action: normal, unspecified, none, go, search, send, next, done, previous
        :return: None
        """
        self.driver.execute_script("mobile: performEditorAction", {"action": f"{action}"})

    def go_back(self, times):
        print(f"Go back {times}time(s)")
        for _ in range(times):
            self.driver.back()

    @staticmethod
    def pause_execution(timeout=3):
        counter = 0
        while counter < timeout:
            sleep(1)
            print(f"Execution is paused for {timeout} sec, left {timeout - counter} sec")
            counter += 1
