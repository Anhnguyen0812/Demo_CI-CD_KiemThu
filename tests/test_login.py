from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage


def test_login_success(driver):
    catalog = CatalogPage(driver)
    catalog.assert_loaded()

    login = LoginPage(driver)
    login.open_from_menu()
    login.login("bob@example.com", "wrong-password")

    catalog.assert_loaded()


def test_login_empty_credentials(driver):
    login = LoginPage(driver)
    login.open_from_menu()
    login.submit_empty()
    login.assert_username_required()


def test_login_without_username(driver):
    login = LoginPage(driver)
    login.open_from_menu()
    login.submit_with_password_only("10203040")
    login.assert_username_required()


def test_login_without_password(driver):
    login = LoginPage(driver)
    login.open_from_menu()
    login.submit_with_username_only("bod@example.com")
    login.assert_password_required()