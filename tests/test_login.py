from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage


def test_login_success(driver):
    catalog = CatalogPage(driver)
    catalog.assert_loaded()

    login = LoginPage(driver)
    login.open_from_menu()
    login.login("bob@example.com", "10203040")

    catalog.assert_loaded()


def test_login_empty_credentials(driver):
    login = LoginPage(driver)
    login.open_from_menu()
    login.submit_empty()
    login.assert_username_required()