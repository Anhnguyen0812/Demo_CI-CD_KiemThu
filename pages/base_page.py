from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
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

    def text_not_present(self, text, timeout=5):
        locator = (AppiumBy.XPATH, f"//*[@text='{text}']")
        short_wait = WebDriverWait(self.driver, timeout)
        return short_wait.until(ec.invisibility_of_element_located(locator))

    def click_text(self, text):
        locator = (AppiumBy.XPATH, f"//*[@text='{text}']")
        self.click(locator)

    def visible_text(self, text):
        locator = (AppiumBy.XPATH, f"//*[@text='{text}']")
        return self.visible(locator)

    def is_text_visible(self, text, timeout=3):
        locator = (AppiumBy.XPATH, f"//*[@text='{text}']")
        try:
            WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_text(self, locator):
        return self.find(locator).text

    def scroll_to_text(self, text):
        ui_selector = (
            'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
            f'.scrollIntoView(new UiSelector().text("{text}").instance(0));'
        )
        return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui_selector)

    def scroll_to_description(self, description):
        ui_selector = (
            'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
            f'.scrollIntoView(new UiSelector().description("{description}").instance(0));'
        )
        return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui_selector)