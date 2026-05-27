# CI/CD Architecture

## 1. Mục tiêu kiến trúc

Pipeline được chia thành các tầng riêng biệt để cân bằng giữa tốc độ, độ ổn định và độ bao phủ:

- Tầng build và unit test để phát hiện lỗi sớm
- Tầng instrumentation test bắt buộc để chặn merge nếu flow quan trọng hỏng
- Tầng Appium smoke để xác nhận luồng điều hướng từ góc nhìn black-box
- Tầng Sauce Labs cloud để mở rộng khả năng chạy trên thiết bị/emulator bên ngoài GitHub runner
- Tầng publish để đóng gói APK theo tag release

## 2. Thành phần hiện tại trong repo

### 2.1 Application layer

- Android app module: `app`
- Build system: Gradle + Android Gradle Plugin `7.4.2`
- Java runtime trong CI dự kiến: `11`

### 2.2 Test layer

- Unit tests trong `app/src/test`
- Instrumentation tests trong `app/src/androidTest`
- Appium host-side test: `AppiumLoginTest`
- Test annotation hiện có:
  - `@HappyFlow`
  - `@ErrorFlow`
  - `@TestOnlyThis`

### 2.3 CI platform

- GitHub Actions là orchestration layer chính
- Android emulator được chạy trên GitHub-hosted runner
- Sauce Labs là tầng cloud test mở rộng, phụ thuộc vào secret

## 3. Kiến trúc workflow đề xuất

```text
Pull Request / Push
        |
        v
Android CI
  |-- Job 1: Build and Unit Tests
  |     |- lintDebug
  |     |- testDebugUnitTest
  |     |- assembleDebug
  |     `- assembleDebugAndroidTest
  |
  |-- Job 2: Mandatory Android Tests
  |     |- Boot emulator
  |     |- Run @HappyFlow
  |     `- Run @ErrorFlow
  |
  `-- Job 3: Sauce Espresso Cloud (optional)
        |- assembleDebug
        |- assembleDebugAndroidTest
        `- saucectl run

Schedule / Manual
        |
        v
Appium Smoke
  |- Build debug APK
  |- Boot emulator
  |- Start Appium server
  `- Run AppiumLoginTest

Tag Push
        |
        v
Publish APK
  |- Set versionCode/versionName
  |- Build APK artifacts
  `- Upload release assets
```

## 4. Nguyên tắc thiết kế

### 4.1 Tách merge gate và smoke gate

Không nên đưa Appium vào merge gate mặc định vì:

- Appium host-side test chậm hơn Espresso
- Khó phân tích flaky hơn instrumentation thuần Android
- Yêu cầu Appium server và lifecycle riêng

Vì vậy:

- Merge gate: build + unit + instrumentation bắt buộc
- Smoke gate: Appium login flow chạy scheduled hoặc manual

### 4.2 Annotation-driven instrumentation

Project đã có sẵn annotation `@HappyFlow` và `@ErrorFlow`. Đây là cơ sở tốt để tách test theo mục đích:

- `@HappyFlow`: flow nghiệp vụ thành công
- `@ErrorFlow`: validation và negative case
- `@TestOnlyThis`: phục vụ debug cục bộ

Khi cần thêm test bắt buộc, ưu tiên gắn annotation thay vì tạo command phức tạp theo class.

### 4.3 Optional cloud execution

Sauce Labs không nên là điều kiện bắt buộc nếu:

- Repo fork không có secrets
- Team chưa mua hoặc chưa cấu hình tài khoản

Workflow cloud vì vậy được đặt là optional, kích hoạt khi có:

- `SAUCE_USERNAME`
- `SAUCE_ACCESS_KEY`

## 5. Test taxonomy để áp dụng

### 5.1 Mandatory tests

Dùng để chặn merge:

- `testDebugUnitTest`
- Instrumentation tests gắn `@HappyFlow`
- Instrumentation tests gắn `@ErrorFlow`

### 5.2 Smoke tests

Dùng để cảnh báo sớm nhưng không nên làm chậm mỗi PR:

- `AppiumLoginTest`

### 5.3 Extended tests

Có thể chạy manual, nightly hoặc release:

- Visual regression tests
- Rotation/device-state tests
- WebView/network-dependent tests nếu có flaky

## 6. Artifact và báo cáo

Mỗi workflow nên upload artifact để debug:

- Test report HTML/XML
- Lint report
- APK và androidTest APK khi cần
- Appium log
- Sauce artifacts

## 7. Branch protection đề xuất

Trạng thái bắt buộc cho branch được bảo vệ:

- `Build and Unit Tests`
- `Mandatory Android Tests`

Không bắt buộc:

- `Sauce Espresso Cloud`
- `Appium Smoke`

## 8. Rủi ro và giới hạn

- AGP `7.4.2` yêu cầu JDK phù hợp, không nên để local env drift quá xa CI env
- Emulator tests có thể tăng thời gian pipeline
- Appium test hiện mới cover login, chưa đại diện cho toàn bộ checkout flow
- Visual tests phụ thuộc secret Sauce và môi trường cloud
