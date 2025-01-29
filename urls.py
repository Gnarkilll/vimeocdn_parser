from selenium import webdriver
from selenium.webdriver.common.by import By

from base import BasePage
from waiting_module.waiter import wait_for_visible

email = ""
password = ""
main_url = ""

class BPLocators:
    EMAIL_INPUT = By.XPATH, "//input[@name='login']"
    PASSWORD_INPUT = By.XPATH, "//input[@name='password']"
    LOGIN_BUTTON = By.XPATH, "//button[@class='main-button']"
    PLAY_BUTTON = By.XPATH, "//button[@class='plyr__control plyr__control--overlaid']"
    URLS = By.XPATH, "//a[contains(@class, 'lectures-list__item')]"


def run():
    driver = webdriver.Chrome()

    session = BasePage(driver)
    session.open(main_url)

    wait_for_visible(driver, BPLocators.EMAIL_INPUT)
    session.set_text(BPLocators.EMAIL_INPUT, email)
    session.set_text(BPLocators.PASSWORD_INPUT, password)
    session.click(BPLocators.LOGIN_BUTTON)
    wait_for_visible(driver, BPLocators.PLAY_BUTTON, timeout=60)
    urls = session.find_elements(BPLocators.URLS)
    urls = [url.get_attribute("href").split("/")[-1] for url in urls]
    print(urls)
    driver.quit()

run()
