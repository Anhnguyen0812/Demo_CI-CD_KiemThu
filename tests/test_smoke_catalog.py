from pages.catalog_page import CatalogPage


def test_open_catalog(driver):
    CatalogPage(driver).assert_loaded()