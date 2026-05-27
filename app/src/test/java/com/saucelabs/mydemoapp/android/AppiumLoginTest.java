package com.saucelabs.mydemoapp.android;

import io.appium.java_client.AppiumBy;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.options.UiAutomator2Options;
import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.net.MalformedURLException;
import java.net.URL;
import java.time.Duration;

public class AppiumLoginTest {
    private static final String APP_ID = "com.saucelabs.mydemoapp.android";

    private AndroidDriver driver;

    @Before
    public void setUp() throws MalformedURLException {
        UiAutomator2Options options = new UiAutomator2Options()
                .setPlatformName("Android")
                .setAutomationName("UiAutomator2")
                .setDeviceName(getEnv("APPIUM_DEVICE_NAME", "Android Emulator"))
                .setAppWaitActivity(APP_ID + ".view.activities.*")
                .setNoReset(false);

        String appPath = System.getenv("APPIUM_APP");
        if (!isNullOrEmpty(appPath)) {
            options.setApp(new File(appPath).getAbsolutePath());
        } else {
            options.setAppPackage(APP_ID)
                    .setAppActivity(APP_ID + ".view.activities.SplashActivity");
        }

        driver = new AndroidDriver(
                new URL(getEnv("APPIUM_SERVER_URL", "http://127.0.0.1:4723/wd/hub")),
                options
        );
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
    }

    @Test
    public void loginFlow() {
        driver.findElement(AppiumBy.accessibilityId("View menu")).click();
        driver.findElement(AppiumBy.xpath("//android.widget.TextView[@content-desc=\"Login Menu Item\"]")).click();
        driver.findElement(AppiumBy.id(APP_ID + ":id/nameET")).sendKeys("bob@example.com");
        driver.findElement(AppiumBy.id(APP_ID + ":id/passwordET")).sendKeys("10203040");
        driver.findElement(AppiumBy.accessibilityId("Tap to login with given credentials")).click();

        Assert.assertTrue(driver.findElement(AppiumBy.id(APP_ID + ":id/productRV")).isDisplayed());
    }

    @After
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }

    private static String getEnv(String key, String fallback) {
        String value = System.getenv(key);
        return isNullOrEmpty(value) ? fallback : value;
    }

    private static boolean isNullOrEmpty(String value) {
        return value == null || value.trim().isEmpty();
    }
}
