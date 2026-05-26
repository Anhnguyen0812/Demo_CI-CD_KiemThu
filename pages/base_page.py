from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator):
        return self.wait.until(ec.presence_of_element_located(locator))

    def click(self, locator):
        self.wait.until(ec.element_to_be_clickable(locator)).click()

    def type(self, locator, value):
        element = self.find(locator)
        element.clear()
        element.send_keys(value)

    def visible(self, locator):
        return self.wait.until(ec.visibility_of_element_located(locator))

    def text_present(self, text):
        locator = (AppiumBy.XPATH, f"//*[@text='{text}']")
        return self.visible(locator)