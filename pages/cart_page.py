from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_TITLE = (AppiumBy.XPATH, "//*[@text='My Cart']")
    CART_LIST = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productRV")
    CHECKOUT_BUTTON = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartBt")

    def assert_loaded(self):
        self.visible(self.CART_TITLE)
        self.visible(self.CART_LIST)

    def assert_product_present(self, product_name):
        self.visible_text(product_name)

    def assert_checkout_visible(self):
        self.visible(self.CHECKOUT_BUTTON)
        self.visible_text("Proceed To Checkout")