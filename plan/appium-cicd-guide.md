# Hướng Dẫn Setup CI/CD Với Appium

Tài liệu này hướng dẫn cách cấu hình CI/CD cho project Android hiện tại để chạy Appium trên GitHub Actions, với mục tiêu chính là kiểm tra khi có pull request vào branch `main`.

## 1. Mục tiêu

Luồng Appium trong project này nên phục vụ các mục tiêu sau:

- Xác nhận app vẫn khởi động và điều hướng được bằng automation black-box
- Kiểm tra một flow smoke quan trọng, ví dụ login
- Không làm merge gate quá chậm hoặc quá flaky
- Có log và artifact để debug khi fail

Với repo này, Appium phù hợp nhất cho smoke test, không nên là lớp test duy nhất trong CI.

## 2. Cách tổ chức workflow nên dùng

Nên chia CI/CD thành 2 lớp:

- `Android CI`: build, lint, unit test, instrumentation test bắt buộc
- `Appium Smoke`: chạy Appium trên emulator

Lý do:

- Espresso/instrumentation ổn định hơn để chặn merge
- Appium chậm hơn và phụ thuộc thêm Appium server
- Nếu đưa toàn bộ Appium vào merge gate ngay từ đầu, pipeline dễ flaky

## 3. Trigger phù hợp cho pull request vào `main`

Nếu bạn muốn workflow chỉ chạy khi có pull request vào `main`, dùng:

```yaml
on:
  pull_request:
    branches:
      - main
```

Nếu bạn muốn chạy thêm khi có push trực tiếp vào `main`, dùng:

```yaml
on:
  pull_request:
    branches:
      - main
  push:
    branches:
      - main
```

Lưu ý:

- `pull_request` và `push` là điều kiện kiểu OR
- Không cần đồng thời có cả PR và push

## 4. File workflow Appium nên dùng

Project hiện đã có workflow:

- `.github/workflows/appium-smoke.yml`

Workflow này có thể dùng làm nền cho Appium CI.

## 5. Cấu trúc workflow Appium

Một workflow Appium cho project này nên gồm các bước:

1. Checkout source code
2. Setup Java
3. Setup Node.js
4. Setup Android SDK
5. Cài Appium và driver `uiautomator2`
6. Build APK debug
7. Khởi động Android emulator
8. Start Appium server
9. Chạy test Appium
10. Upload report và log

Ví dụ cấu hình:

```yaml
name: Appium Smoke

on:
  pull_request:
    branches:
      - main

permissions:
  contents: read

jobs:
  appium-smoke:
    runs-on: ubuntu-latest
    timeout-minutes: 35
    env:
      APPIUM_SERVER_URL: http://127.0.0.1:4723/wd/hub
      APPIUM_DEVICE_NAME: Android Emulator
      APPIUM_APP: ${{ github.workspace }}/app/build/outputs/apk/debug/app-debug.apk

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '11'
          cache: gradle

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Setup Android SDK
        uses: android-actions/setup-android@v3

      - name: Install Appium
        run: |
          npm install -g appium
          appium driver install uiautomator2

      - name: Build debug APK
        run: |
          chmod +x gradlew
          ./gradlew assembleDebug

      - name: Run Appium smoke test
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 31
          arch: x86_64
          profile: pixel_6
          script: |
            adb wait-for-device
            appium --base-path /wd/hub > appium.log 2>&1 &
            ./gradlew testDebugUnitTest -PincludeAppiumTests=true --tests com.saucelabs.mydemoapp.android.AppiumLoginTest

      - name: Upload Appium reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: appium-smoke-artifacts
          path: |
            appium.log
            app/build/reports/tests/
```

## 6. Giải thích cấu hình hiện tại của project

Project hiện đã được chỉnh để `AppiumLoginTest` không chạy cùng unit test mặc định.

Trong `app/build.gradle`, Appium test chỉ chạy khi truyền:

```bash
-PincludeAppiumTests=true
```

Điều này giúp:

- `testDebugUnitTest` bình thường không bị fail do thiếu Appium server
- Appium chỉ chạy khi workflow Appium chủ động gọi

## 7. Test Appium hiện tại hoạt động thế nào

File test hiện tại:

- `app/src/test/java/com/saucelabs/mydemoapp/android/AppiumLoginTest.java`

Test này:

- mở app
- mở menu
- vào màn hình login
- nhập username/password
- submit
- xác nhận quay về product catalog

Các biến môi trường test đang dùng:

- `APPIUM_SERVER_URL`
- `APPIUM_DEVICE_NAME`
- `APPIUM_APP`

Nếu `APPIUM_APP` không có, test sẽ fallback sang mở app bằng package/activity.

## 8. Có nên chạy Appium trên mọi pull request không

Có 2 cách:

### Cách 1: Chạy Appium ở mọi PR vào `main`

Phù hợp khi:

- team muốn smoke test black-box luôn chạy
- số lượng test Appium ít
- chấp nhận pipeline chậm hơn

Ưu điểm:

- phát hiện sớm lỗi integration

Nhược điểm:

- tăng thời gian CI
- dễ bị flaky hơn Espresso

### Cách 2: Chỉ chạy Appium manual hoặc nightly

Phù hợp khi:

- team muốn merge gate ổn định trước
- Appium mới ở mức thử nghiệm

Ưu điểm:

- merge nhanh hơn
- ít fail giả hơn

Nhược điểm:

- lỗi black-box có thể được phát hiện muộn hơn

Khuyến nghị cho project này:

- Dùng Espresso làm merge gate bắt buộc
- Dùng Appium như smoke test riêng
- Nếu Appium ổn định sau một thời gian, mới cân nhắc thêm vào PR gate

## 9. Có cần secrets không

Nếu chỉ chạy Appium local emulator trên GitHub-hosted runner:

- Không cần secret riêng

Nếu muốn chạy thêm Sauce Labs:

- Cần `SAUCE_USERNAME`
- Cần `SAUCE_ACCESS_KEY`

## 10. Bật branch protection

Sau khi workflow đã chạy ổn định trên GitHub:

1. Vào `Settings`
2. Chọn `Branches`
3. Tạo rule cho `main`
4. Bật `Require a pull request before merging`
5. Bật `Require status checks to pass before merging`

Nếu Appium đã đủ ổn định, có thể chọn thêm check:

- `appium-smoke`

Nếu chưa ổn định, chỉ nên bắt buộc:

- `Build and Unit Tests`
- `Mandatory Android Tests`

## 11. Trình tự setup thực tế

Nên làm theo thứ tự:

1. Xác nhận `Android CI` chạy ổn
2. Chạy `Appium Smoke` bằng `workflow_dispatch`
3. Kiểm tra artifact `appium.log`
4. Sửa flaky nếu có
5. Đổi trigger sang `pull_request` vào `main` nếu muốn
6. Bật branch protection

## 12. Các lỗi thường gặp

### Appium server không lên

Dấu hiệu:

- test fail ngay khi tạo `AndroidDriver`

Cách xử lý:

- kiểm tra bước `appium --base-path /wd/hub`
- đọc `appium.log`

### Emulator chưa sẵn sàng

Dấu hiệu:

- không tìm thấy app hoặc session start fail

Cách xử lý:

- giữ `adb wait-for-device`
- tránh chạy test trước khi emulator boot xong

### Sai đường dẫn APK

Dấu hiệu:

- Appium báo không tìm thấy app

Cách xử lý:

- kiểm tra `APPIUM_APP`
- bảo đảm `./gradlew assembleDebug` đã chạy thành công

### Test pass local nhưng fail trên CI

Nguyên nhân thường gặp:

- local dùng thiết bị thật, CI dùng emulator
- local đã login sẵn hoặc còn state cũ
- selector mong manh

Cách xử lý:

- giữ test id ổn định
- tránh phụ thuộc state cũ
- dùng assertion rõ ràng sau mỗi bước quan trọng

## 13. Khuyến nghị cuối cùng

Với project này, phương án thực dụng nhất là:

- PR vào `main` chạy `Android CI`
- Appium chạy ở workflow riêng
- Sau khi Appium ổn định, đổi trigger của `appium-smoke.yml` sang:

```yaml
on:
  pull_request:
    branches:
      - main
```

Như vậy bạn có thể rollout an toàn, không khóa merge gate quá sớm bằng một lớp test còn dễ flaky.
