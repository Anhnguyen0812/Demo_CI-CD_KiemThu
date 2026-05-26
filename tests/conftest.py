import os
import sys
from datetime import datetime

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def pytest_configure(config):
    for path in ("screenshots", "reports", "logs"):
        os.makedirs(path, exist_ok=True)


@pytest.fixture
def driver():
    apk_path = os.getenv("APK_PATH")
    server_url = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
    device_name = os.getenv("DEVICE_NAME", "Android Device")
    platform_name = os.getenv("PLATFORM_NAME", "Android")
    automation_name = os.getenv("AUTOMATION_NAME", "UiAutomator2")

    if not apk_path or not os.path.exists(apk_path):
        raise FileNotFoundError(f"APK_PATH khong hop le: {apk_path}")

    options = UiAutomator2Options()
    options.platform_name = platform_name
    options.device_name = device_name
    options.automation_name = automation_name
    options.app = apk_path
    options.auto_grant_permissions = True
    options.no_reset = False
    options.app_wait_activity = "com.saucelabs.mydemoapp.android.view.activities.*"

    driver = webdriver.Remote(server_url, options=options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = item.name.replace("/", "_").replace("\\", "_")
            path = os.path.join("screenshots", f"{name}_{timestamp}.png")
            driver.save_screenshot(path)