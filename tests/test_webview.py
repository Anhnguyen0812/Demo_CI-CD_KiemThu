from pages.webview_page import WebViewPage


def test_webview_without_url_shows_error(driver):
    webview = WebViewPage(driver)
    webview.open_from_menu()
    webview.submit_empty()
    webview.assert_invalid_url_error()


def test_webview_valid_url_hides_error(driver):
    webview = WebViewPage(driver)
    webview.open_from_menu()
    webview.open_url("https://www.google.com")
    webview.assert_no_invalid_url_error()