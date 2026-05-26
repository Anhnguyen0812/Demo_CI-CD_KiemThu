from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class CatalogPage(BasePage):
    PRODUCT_LIST = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productRV")
    MENU_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "View menu")

    def assert_loaded(self):
        self.visible(self.MENU_BUTTON)
        self.visible(self.PRODUCT_LIST)