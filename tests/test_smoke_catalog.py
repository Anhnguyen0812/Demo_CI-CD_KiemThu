from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.product_detail_page import ProductDetailPage


def test_open_catalog(driver):
    CatalogPage(driver).assert_loaded()


def test_open_product_detail(driver):
    catalog = CatalogPage(driver)
    catalog.assert_loaded()
    catalog.open_backpack()

    detail = ProductDetailPage(driver)
    detail.assert_backpack_loaded()


def test_add_product_to_cart(driver):
    catalog = CatalogPage(driver)
    catalog.assert_loaded()
    catalog.open_backpack()

    detail = ProductDetailPage(driver)
    detail.assert_backpack_loaded()
    detail.increase_quantity()
    detail.assert_quantity(2)
    detail.add_to_cart()

    catalog.open_cart()

    cart = CartPage(driver)
    cart.assert_loaded()
    cart.assert_product_present("Sauce Labs Backpack")
    cart.assert_checkout_visible()