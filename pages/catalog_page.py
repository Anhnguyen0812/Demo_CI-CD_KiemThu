from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class CatalogPage(BasePage):
    PRODUCT_LIST = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productRV")
    MENU_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "View menu")
    CART_BUTTON = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartRL")
    BACKPACK_TITLE = (AppiumBy.XPATH, "//*[@text='Sauce Labs Backpack']")

    def assert_loaded(self):
        self.visible(self.MENU_BUTTON)
        self.visible(self.PRODUCT_LIST)

    def open_backpack(self):
        self.click(self.BACKPACK_TITLE)

    def open_cart(self):
        self.click(self.CART_BUTTON)