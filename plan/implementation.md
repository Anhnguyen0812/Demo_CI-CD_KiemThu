# CI/CD Implementation Plan

## 1. Phạm vi

Tài liệu này mô tả các bước cần thực hiện để đưa pipeline CI/CD vào vận hành ổn định trên GitHub Actions.

## 2. Đầu ra mong đợi

Sau khi hoàn tất:

- Pull request có merge gate rõ ràng
- App build được và test có artifact để truy vết
- Mandatory test được tách khỏi smoke test
- Team có thể bật branch protection trên GitHub

## 3. File đã/nên sử dụng

- `.github/workflows/ci.yml`
- `.github/workflows/appium-smoke.yml`
- `.github/workflows/publish-on-release.yml`
- `.sauce/config.yml`
- `app/build.gradle`
- `app/src/test/java/com/saucelabs/mydemoapp/android/AppiumLoginTest.java`

## 4. Checklist triển khai

### 4.1 GitHub Actions

1. Tạo workflow `Android CI`
2. Tạo workflow `Appium Smoke`
3. Nâng cấp action version cho workflow publish
4. Upload artifact cho các job quan trọng

### 4.2 Gradle và test control

1. Loại Appium test khỏi unit gate mặc định
2. Cho phép opt-in bằng property `includeAppiumTests`
3. Sử dụng annotation filter cho instrumentation tests

### 4.3 Secrets và environment

Cần tạo secrets sau nếu muốn chạy Sauce Labs:

- `SAUCE_USERNAME`
- `SAUCE_ACCESS_KEY`

Không cần secrets riêng cho Appium smoke local emulator trên GitHub-hosted runner.

### 4.4 Branch protection

Cần cấu hình trên GitHub repository settings:

1. Protect branch `main` hoặc `master`
2. Require status checks before merging
3. Chọn:
   - `Build and Unit Tests`
   - `Mandatory Android Tests`

## 5. Trình tự rollout đề xuất

### Phase 1: Baseline

- Merge workflow `Android CI`
- Chạy trên pull request
- Xác định test nào đang flaky

Tiêu chí đạt:

- Build thành công ổn định
- Mandatory instrumentation chạy được trên emulator

### Phase 2: Smoke hardening

- Merge workflow `Appium Smoke`
- Chạy `workflow_dispatch` trước
- Sau khi ổn định mới bật `schedule`

Tiêu chí đạt:

- `AppiumLoginTest` không phụ thuộc thiết bị local
- Appium log đủ để debug khi fail

### Phase 3: Cloud expansion

- Cấu hình `SAUCE_USERNAME` và `SAUCE_ACCESS_KEY`
- Xác nhận `.sauce/config.yml` còn phù hợp với thiết bị mong muốn
- Đánh giá có nên giữ cloud job trong PR hay chỉ release/nightly

Tiêu chí đạt:

- Sauce cloud run tạo artifact đúng
- Không làm nghẽn merge gate nếu cloud có vấn đề tạm thời

## 6. Quy ước viết test từ nay

### 6.1 Khi nào dùng `@HappyFlow`

Gắn cho test cover đường đi nghiệp vụ chính:

- login thành công
- thêm vào giỏ
- checkout thành công

### 6.2 Khi nào dùng `@ErrorFlow`

Gắn cho test validation và lỗi dữ liệu:

- bỏ trống username/password
- sai format URL
- lỗi form checkout

### 6.3 Khi nào dùng Appium

Dùng Appium cho:

- smoke test black-box
- cross-tool validation
- flow cần tương tác ở mức automation framework độc lập với Espresso

Không dùng Appium cho mọi test giao diện nhỏ, vì sẽ làm CI chậm và khó ổn định hơn.

## 7. Vấn đề cần theo dõi sau rollout

- Thời gian trung bình mỗi workflow
- Tỉ lệ flaky của emulator tests
- Tỉ lệ fail do hạ tầng và do ứng dụng
- Khả năng tái sử dụng annotation taxonomy khi test suite tăng

## 8. Công việc tiếp theo đề nghị

1. Gắn thêm annotation cho các test chưa được phân loại
2. Tách visual tests thành workflow riêng
3. Thêm badge workflow vào `README.md`
4. Nếu cần, thêm nightly full regression
