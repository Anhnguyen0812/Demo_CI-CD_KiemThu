from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    PRODUCT_TITLE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productTV")
    QUANTITY_TEXT = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/noTV")
    PLUS_BUTTON = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/plusIV")
    ADD_TO_CART_BUTTON = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartBt")

    def assert_backpack_loaded(self):
        self.visible_text("Sauce Labs Backpack")
        self.visible(self.ADD_TO_CART_BUTTON)

    def increase_quantity(self):
        self.click(self.PLUS_BUTTON)

    def assert_quantity(self, expected):
        actual = self.get_text(self.QUANTITY_TEXT)
        assert actual == str(expected), f"Expected quantity {expected}, got {actual}"

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)