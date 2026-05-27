from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class WebViewPage(BasePage):
    MENU_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "View menu")
    URL_INPUT = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/urlET")
    GO_BUTTON = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/goBtn")

    def open_from_menu(self):
        self.click(self.MENU_BUTTON)
        self.click_text("WebView")

    def submit_empty(self):
        self.click(self.GO_BUTTON)

    def open_url(self, url):
        self.type(self.URL_INPUT, url)
        self.click(self.GO_BUTTON)

    def assert_invalid_url_error(self):
        self.text_present("Please provide a correct https url.")

    def assert_no_invalid_url_error(self):
        assert self.text_not_present("Please provide a correct https url.")