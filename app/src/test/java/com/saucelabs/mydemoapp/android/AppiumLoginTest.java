package com.saucelabs.mydemoapp.android;
import io.appium.java_client.AppiumBy;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.options.UiAutomator2Options;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import java.net.MalformedURLException;
import java.net.URL;
import java.time.Duration;

public class AppiumLoginTest {
    public AndroidDriver driver;

    @Before
    public void setUp() throws MalformedURLException {
        UiAutomator2Options options = new UiAutomator2Options()
                .setDeviceName("LMV6001868dd95") // Thay bằng ID từ lệnh adb devices
                .setAppPackage("com.saucelabs.mydemoapp.android")
                .setAppActivity("com.saucelabs.mydemoapp.android.view.activities.MainActivity")
                .setNoReset(true);

        driver = new AndroidDriver(new URL("http://127.0.0.1:4723"), options);
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
    }

    @Test
    public void loginFlow() {
        // 1. Nhấn vào biểu tượng Menu (Hamburger icon)
        driver.findElement(AppiumBy.accessibilityId("View menu")).click();

        // 2. Nhấn vào dòng chữ "Log In" trong menu sidebar
        // Lưu ý: Dùng XPath để tìm chính xác phần tử có thuộc tính text là Log In
        driver.findElement(AppiumBy.xpath("//android.widget.TextView[@content-desc=\"Login Menu Item\"]")).click();

        // 3. Nhập Username (ID này soi từ Appium Inspector)
        driver.findElement(AppiumBy.id("com.saucelabs.mydemoapp.android:id/nameET")).sendKeys("bob@example.com");

        // 4. Nhập Password
        driver.findElement(AppiumBy.id("com.saucelabs.mydemoapp.android:id/passwordET")).sendKeys("10203040");

        // 5. Nhấn nút Login
        driver.findElement(AppiumBy.accessibilityId("Tap to login with given credentials")).click();

        // Đợi 2 giây để quan sát kết quả
        try { Thread.sleep(2000); } catch (InterruptedException e) { e.printStackTrace(); }
    }

    @After
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}