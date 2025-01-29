import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 10


class Wait(WebDriverWait):
    ERR_MSG = None
    LOG_MSG = None

    def until(self, method, **kwargs):
        """Calls the method provided with the driver as an argument until the \
        return value is not False."""
        screen = None
        stacktrace = None

        end_time = time.time() + self._timeout
        while True:
            try:
                print(Wait.LOG_MSG)
                value = method(self._driver)
                if value:
                    return value
            except self._ignored_exceptions as exc:
                screen = getattr(exc, 'screen', None)
                stacktrace = getattr(exc, 'stacktrace', None)
            time.sleep(self._poll)
            if time.time() > end_time:
                break
        raise TimeoutException(Wait.ERR_MSG, screen, stacktrace)


def get_type_of_wait(wait_type, locator_or_obj, **kwargs):
    def presence_of_element_located(): return ec.presence_of_element_located(locator_or_obj)

    def visibility_of_element_located(): return ec.visibility_of_element_located(locator_or_obj)

    def invisibility_of_element_located(): return ec.invisibility_of_element_located(locator_or_obj)

    def element_to_be_clickable(): return ec.element_to_be_clickable(locator_or_obj)

    def text_to_be_present_in_element(): return ec.text_to_be_present_in_element(locator_or_obj, **kwargs)

    def number_of_windows_to_be(): return ec.number_of_windows_to_be(locator_or_obj)

    def title_is(): return ec.title_is(locator_or_obj)

    def url_contains(): return ec.url_contains(locator_or_obj)

    def unknown_waiter(): return "Unknown waiter"

    wait_types = dict(
        presence_of_element_located=presence_of_element_located,
        visibility_of_element_located=visibility_of_element_located,
        invisibility_of_element_located=invisibility_of_element_located,
        element_to_be_clickable=element_to_be_clickable,
        text_to_be_present_in_element=text_to_be_present_in_element,
        number_of_windows_to_be=number_of_windows_to_be,
        title_is=title_is,
        url_contains=url_contains
    )

    return wait_types.get(wait_type, unknown_waiter)()


def wait_for(driver, wait_type, locator_or_obj, timeout, **kwargs):
    Wait(driver, timeout).until(get_type_of_wait(wait_type, locator_or_obj, **kwargs))


def wait_for_visible(driver, locator, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"Element {locator} is not visible after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for visible: {locator}"
    wait_for(driver, "visibility_of_element_located", locator, timeout)


def wait_for_not_visible(driver, locator, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"Element {locator} is visible after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for not visible: {locator}"
    wait_for(driver, "invisibility_of_element_located", locator, timeout)


def wait_for_presence(driver, locator, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"Element {locator} is not presence after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for presence: {locator}"
    wait_for(driver, "presence_of_element_located", locator, timeout)


def wait_for_clickable(driver, locator, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"Element {locator} is not clickable after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for clickable: {locator}"
    wait_for(driver, "element_to_be_clickable", locator, timeout)


def wait_for_text_to_be_present(driver, locator, text, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"Text '{text}' is not presented for {locator} after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for text '{text}' to be present for {locator}"
    wait_for(driver, "text_to_be_present_in_element", locator, timeout, text_=text)


def wait_for_attr_contains_text(driver, locator, attr, text, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"Attribute '{attr}' does not contain text '{text}' for {locator} after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for attribute '{attr}' contains text '{text}' for {locator}"
    wait_for(driver, "attr_contains_text", locator, timeout, attr=attr, text=text)


def wait_for_attr_contains_value(driver, locator, attr, value, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"Attribute '{attr}' does not contain value '{value}' for {locator} after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for attribute '{attr}' contains value '{value}' for {locator}"
    wait_for(driver, "attr_contains_value", locator, timeout, attr=attr, value=value)


def wait_for_css_property_contains_value(driver, locator, css_property, value, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"CSS property '{css_property}' does not contain value '{value}' for {locator} after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for CSS property '{css_property}' contains value '{value}' for {locator}"
    wait_for(driver, "css_property_contains_value", locator, timeout, css_property=css_property, value=value)


def wait_for_amount_of_web_elements_equals(driver, locator, expected, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"Amount of web elements is not equal '{expected}' for {locator} after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for amount of web elements equals '{expected}' for {locator}"
    wait_for(driver, "amount_of_web_elements_equals", locator, timeout, expected=expected)


def wait_for_number_of_windows(driver, number_of_windows, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"Number of windows is not equal '{number_of_windows}' after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for number of windows: {number_of_windows}"
    wait_for(driver, "number_of_windows_to_be", number_of_windows, timeout)


def wait_for_title_is(driver, title, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"Title is not equal '{title}' after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for title is: {title}"
    wait_for(driver, "title_is", title, timeout)


def wait_for_url_contains(driver, expected_string, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"URL does not contain '{expected_string}' after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for URL contains: {expected_string}"
    wait_for(driver, "url_contains", expected_string, timeout)


def wait_for_attr_value_is_not_empty(driver, locator, attr, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"Attribute '{attr}' is empty for {locator} after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for attribute '{attr}' is not empty for {locator}"
    wait_for(driver, "attr_value_is_not_empty", locator, timeout, attr=attr)


def wait_for_alert_is_present(driver, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"Alert is not presented after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for alert is presented"
    Wait(driver, timeout).until(ec.alert_is_present())


def wait_for_page_load(driver, timeout=DEFAULT_TIMEOUT):
    Wait.ERR_MSG = f"Page was not loaded after {timeout} seconds"
    Wait.LOG_MSG = f"Wait for page to load"
    Wait(driver, timeout).until(lambda driver:
                                driver.execute_script('return document.readyState') == 'complete')
