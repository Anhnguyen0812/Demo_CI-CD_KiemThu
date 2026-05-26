from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class LoginPage(BasePage):
    MENU_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "View menu")
    LOGIN_MENU_ITEM = (AppiumBy.XPATH, "//android.widget.TextView[@content-desc='Login Menu Item']")
    USERNAME_INPUT = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameET")
    PASSWORD_INPUT = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/passwordET")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Tap to login with given credentials")

    def open_from_menu(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGIN_MENU_ITEM)

    def login(self, username, password):
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def submit_empty(self):
        self.click(self.LOGIN_BUTTON)

    def assert_username_required(self):
        self.text_present("Username is required")